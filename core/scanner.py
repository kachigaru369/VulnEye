# core/scanner.py (نسخه بهبود یافته با fallback سِلنیوم)

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from payloads import sqli, xss
from core.selenium_scanner import scan_with_browser

def scan_page(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        forms = soup.find_all("form")

        if not forms:
            print(f"[scanner] فرمی در {url} پیدا نشد.")
            return

        print(f"[scanner] پیدا شد {len(forms)} فرم در {url}")

        for form in forms:
            action = form.get("action") or url
            method = form.get("method", "get").lower()
            inputs = form.find_all("input")

            form_url = urljoin(url, action)
            input_names = [i.get("name") for i in inputs if i.get("name")]

            print(f"  ↳ فرم ({method.upper()}) → {form_url}")
            print(f"    ↳ فیلدها: {input_names}")

            is_login_form = (
                'login' in form.get('id', '').lower()
                or any("user" in name.lower() or "pass" in name.lower() for name in input_names)
            )
            is_search_form = (
                any("search" in name.lower() or name.lower() == "q" for name in input_names)
            )

            if is_login_form:
                print("    ⤷ فرم login شناسایی شد. اجرای تست SQLi...")
                result = sqli.test_sqli(form_url, method, input_names)
                if result == "fallback":
                    print("    ⤷ اجرا با Selenium به عنوان fallback...")
                    scan_with_browser(url)
            elif is_search_form:
                print("    ⤷ فرم جستجو شناسایی شد. اجرای تست XSS...")
                xss.test_xss(form_url, method, input_names)
            else:
                print("    ⤷ فرم ناشناس. فعلاً رد شد.")

    except Exception as e:
        print(f"[scanner] خطا در بررسی {url}: {e}")


def manual_attack(target_url, attack_type):
    if attack_type.lower() == "sqli":
        sqli.test_sqli_direct(target_url)
    elif attack_type.lower() == "xss":
        xss.test_xss_direct(target_url)
    else:
        print(f"[scanner] نوع حمله ناشناخته: {attack_type}")
