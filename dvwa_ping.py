import requests

url = "http://192.168.0.187/dvwa/login.php"

try:
    res = requests.get(url)
    if res.status_code == 200:
        print("[+] connected !")
    else:
        print(f"[-] unexpected error {res.status_code}")
except Exception as e:
    print(f"[-] error in connecting : {e}")