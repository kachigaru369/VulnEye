import requests
from bs4 import BeautifulSoup
# import pickle
from urllib.parse import urljoin


# لیست اسم‌های احتمالی برای فیلد یوزرنیم و پسورد
USERNAME_KEYS = ['username', 'user', 'email', 'login']
PASSWORD_KEYS = ['password', 'pass', 'passwd']


def find_login_fields(soup):
    form = soup.find('form')
    if not form:
        print("[!] No form found.")
        return None

    action = form.get('action')
    method = form.get('method', 'get').lower()
    inputs = form.find_all('input')

    user_field = None
    pass_field = None
    submit_field = None
    other_fields = {}

    for input_tag in inputs:
        name = input_tag.get('name', '')
        input_type = input_tag.get('type', '').lower()

        # فیلد یوزرنیم
        if not user_field and any(key in name.lower() for key in USERNAME_KEYS):
            user_field = name

        # فیلد پسوورد
        elif not pass_field and input_type == 'password':
            pass_field = name

        # دکمه ثبت
        elif input_type in ['submit', 'button'] and not submit_field:
            submit_field = name or 'submit'

        # بقیه فیلدها (مثل توکن CSRF و غیره)
        elif name:
            value = input_tag.get('value', '')
            other_fields[name] = value

    return {
        'action': action,
        'method': method,
        'username': user_field,
        'password': pass_field,
        'submit': submit_field,
        'others': other_fields
    }

# def login_to_site(url):
#     session = requests.Session()

#     # دریافت HTML اولیه
#     response = session.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     form_data = find_login_fields(soup)
#     if not form_data:
#         return

#     # گرفتن اطلاعات از کاربر
#     user_value = input("Enter username: ")
#     pass_value = input("Enter password: ")
#     cookies_dict = session.cookies.get_dict()

#     post_data = form_data['others']
#     post_data[form_data['username']] = user_value
#     post_data[form_data['password']] = pass_value
#     post_data[cookies_dict['PHPSESSID']] = cookies_dict['PHPSESSID']

#     if form_data['submit']:
#         post_data[form_data['submit']] = 'Submit'

#     # ساختن URL کامل (نسبی یا مطلق)
#     login_url = form_data['action']
#     if not login_url.startswith("http"):
#         from urllib.parse import urljoin
#         login_url = urljoin(url, login_url)

#     # ارسال درخواست POST برای لاگین
#     print("[*] Sending login request to:", login_url)
#     if form_data['method'] == 'post':
#         login_response = session.post(login_url, data=post_data)
#     else:
#         login_response = session.get(login_url, params=post_data)

#     # print("[+] Login attempted. Final URL:", login_response.url)
#     print("[+] Response code:", login_response.status_code)
#     # print("[+] Partial response preview:\n")
#     global last_responce 
#     last_responce = login_response.text
#     # print(last_responce)  # نمایش اولین بخش پاسخ
#     # cookies_dict = session.cookies.get_dict()
#     # my_cookie = cookies_dict['PHPSESSID']



def login_to_site(url):
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    form_data = find_login_fields(soup)
    if not form_data:
        return None, None

    user_value = input("Enter username: ")
    pass_value = input("Enter password: ")

    post_data = form_data['others']
    post_data[form_data['username']] = user_value
    post_data[form_data['password']] = pass_value

    if form_data['submit']:
        post_data[form_data['submit']] = 'Submit'

    login_url = form_data['action']
    if not login_url.startswith("http"):
        login_url = urljoin(url, login_url)

    print("[*] Sending login request to:", login_url)

    if form_data['method'] == 'post':
        login_response = session.post(login_url, data=post_data)
    else:
        login_response = session.get(login_url, params=post_data)

    print("[+] Response code:", login_response.status_code)

    # بررسی موفقیت لاگین
    if is_login_successful(login_response):
        cookies_dict = session.cookies.get_dict()
        last_responce = login_response.text
        return cookies_dict, session #, last_responce
    else:
        print("[!] Login failed.")
        return None, None #, None





def is_login_successful(response):
    failed_indicators = ["invalid", "wrong password", "login failed", "try again"]
    if any(word in response.text.lower() for word in failed_indicators):
        return False
    if "login" in response.url.lower():
        return False
    return True





# def load_session():

#     session = requests.Session()
#     try:
#         with open("cookies.pkl", "rb") as f:
#             session.cookies.update(pickle.load(f))
#         print("[*] Loaded session from saved cookies.")
#     except FileNotFoundError:
#         print("[!] No saved cookies found.")
#     return session


# login_to_site("http://example.com/login")

# if __name__ == "__main__":
#     login_to_site()
