import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ai_assistants.form_classifier import extract_inputs_from_html, classify_form
import html_field_finder  # فایل جداگانه‌ای که login_to_site و find_login_fields در آن است
from ai_assistants.vuln_predictor import predict_vulnerabilities


def is_login_form_present(html):
    login_keywords = [
        "login", "log-in", "log_in", "signin", "sign-in", "sign_in",
        "username", "user", "userid", "user-id", "user_name", "email", "e-mail",
        "password", "pass", "pwd", "passwd", "input type=\"password\"",
        "remember me", "forgot password", "reset password",
        "login to your account", "sign in to your account"
    ]
    return any(k in html.lower() for k in login_keywords)


def analyze_forms_with_ai(session, url):
    print("analyzing forms with ai...")
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all("form")

    print(f"\n[*] Found {len(forms)} form(s). Analyzing with AI...")
    for i, form in enumerate(forms):
        inputs = extract_inputs_from_html(str(form))

        print(f"  [DEBUG] Raw inputs: {inputs}")

        form_type = classify_form(inputs)
        
        vulns = predict_vulnerabilities(form_type)
    print(f"[Form {i+1}] Type Detected by AI: {form_type}")
    if vulns:
        print(f"  ↳ Possible Vulnerabilities: {', '.join(vulns)}")
    else:
        print(f"  ↳ No known vulnerabilities mapped to this form type.")


        print(f"[Form {i+1}] Type Detected by AI: {form_type}")
    
    

# مکان شروع حمله!!!!!!!!!!!!!!!!!!!!!!!!!

    # if form_type == "command":
    # from core import CommandInjection
    # print("[*] Launching Command Injection module...")
    # CommandInjection.starter(url, session)



def intelligent_login_handler():
    url = input("Enter the target URL: ").strip()

    # مرحله ۱: بررسی اینکه فرم login وجود دارد یا نه
    raw_html = requests.get(url).text
    if is_login_form_present(raw_html):
        print("[*] Possible login form detected.")
        
        while True:
            ask = input("[?] Does this page require login to access your target data? (yes/no): ").strip().lower()
            if ask in ["yes", "y"]:
                print("[*] trying to login to site...")
                cookies, session = html_field_finder.login_to_site(url)
                if session:
                    analyze_forms_with_ai(session, url)
                else:
                    print("[!] Login failed. Cannot continue.")
                break
            elif ask in ["no", "n"]:
                print("[*] Skipping login. Analyzing public content...")
                session = requests.Session()
                analyze_forms_with_ai(session, url)
                break
            else:
                print("[!] Invalid input. Please enter 'yes' or 'no'.")

        # ask = input("[?] Does this page require login to access your target data? (yes/no): ").strip().lower()
        # if ask in ["yes", "y"]:
        #     print("[*] trying to login to site...")
        #     cookies, session = html_field_finder.login_to_site(url)
        #     if session:
        #         analyze_forms_with_ai(session, url)
        #     else:
        #         print("[!] Login failed. Cannot continue.")
        # else:
        #     print("[*] Skipping login. Analyzing public content...")
        #     session = requests.Session()
        #     analyze_forms_with_ai(session, url)
    else:
        print("[*] No login form detected. Scanning directly...")
        session = requests.Session()
        analyze_forms_with_ai(session, url)


if __name__ == "__main__":
    intelligent_login_handler()
