form_vuln_map = {
    "login": [
        "SQL Injection", "SQL Injection (Blind)", "Brute Force", 
        "Weak Session IDs", "Authorisation Bypass", "CSRF"
    ],
    "signup": [
        "SQL Injection", "Insecure CAPTCHA", "CSRF", 
        "Weak Session IDs", "Cryptography"
    ],
    "search": [
        "SQL Injection", "XSS (Reflected)", "Open HTTP Redirect"
    ],
    "comment": [
        "XSS (Stored)", "CSRF", "CSP Bypass"
    ],
    "contact": [
        "XSS (Reflected)", "Email Injection", "CSRF"
    ],
    "upload": [
        "File Upload", "File Inclusion", "Command Injection"
    ],
    "command": [
        "Command Injection"
    ],
    "api": [
        "API", "Authorisation Bypass", "Cryptography"
    ],
    "unknown": []
}


def predict_vulnerabilities(form_type: str) -> list[str]:
    return form_vuln_map.get(form_type.lower(), [])
