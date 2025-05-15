import requests
from bs4 import BeautifulSoup
import RedirectionScanner


CMDI_FIELD_KEYS = [
    'cmd', 'command', 'exec', 'execute', 'run', 'ip', 'host',
    'target', 'ping', 'traceroute', 'dns', 'address', 'lookup', 'server'
]


from bs4 import BeautifulSoup
import requests

# لیست فیلدهای مشکوک برای Command Injection
CMDI_FIELD_KEYS = [
    'cmd', 'command', 'exec', 'execute', 'run', 'run_cmd', 'shell', 'bash',
    'ip', 'host', 'target', 'address', 'server', 'dns', 'gateway',
    'router', 'lookup', 'resolve', 'ping', 'traceroute', 'param', 'input'
]


SUBMIT_FIELD_KEYS = [
    'submit', 'Submit', 'submit_btn', 'submit_button',
    'send', 'Send', 'go', 'Go', 'proceed', 'confirm',
    'execute', 'run', 'run_cmd', 'launch', 'start'
]




# def find_cmdi_inputs(url, session):
#     response = session.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     forms = soup.find_all('form')
#     suspicious_fields = []

#     for form in forms:
#         inputs = form.find_all('input')
#         for i in inputs:
#             name = i.get('name', '').lower()
#             id_ = i.get('id', '').lower()
#             placeholder = i.get('placeholder', '').lower()
#             field_info = f"name={name} id={id_} placeholder={placeholder}"

#             if any(key in name for key in CMDI_FIELD_KEYS) or \
#                any(key in id_ for key in CMDI_FIELD_KEYS) or \
#                any(key in placeholder for key in CMDI_FIELD_KEYS):
#                 suspicious_fields.append(field_info)

#     if suspicious_fields:
#         print("[+] Possible command injection input fields:")
#         for field in suspicious_fields:
#             print("   -", field)
#     else:
#         print("[-] No suspicious CMDi-related input fields found.")

def starter():
    check_redir()

def find_cmdi_inputs(url, session):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    forms = soup.find_all('form')
    suspicious_fields = []
    submit_buttons = []

    for form in forms:
        inputs = form.find_all('input')
        for i in inputs:
            input_type = i.get('type', '').lower()
            name = i.get('name', '').lower()
            id_ = i.get('id', '').lower()
            placeholder = i.get('placeholder', '').lower()

            if input_type in SUBMIT_FIELD_KEYS:
                submit_buttons.append((name, i.get('value', '')))
            
            field_info = f"name={name} id={id_} placeholder={placeholder}"
            if any(key in name for key in CMDI_FIELD_KEYS) or \
               any(key in id_ for key in CMDI_FIELD_KEYS) or \
               any(key in placeholder for key in CMDI_FIELD_KEYS):
                suspicious_fields.append(field_info)

    if suspicious_fields:
        print("[+] Possible command injection input fields:")
        for field in suspicious_fields:
            print("   -", field)
    else:
        print("[-] No suspicious CMDi-related input fields found.")

    if submit_buttons:
        print("[*] Detected submit/button fields:")
        for name, val in submit_buttons:
            print(f"   - name={name} value={val}")

    return suspicious_fields, submit_buttons


def check_redir():
    url, session = RedirectionScanner.redirection_scanner()
    if session:
        find_cmdi_inputs(url, session)



# if __name__ == "__main__":
#     starter()
