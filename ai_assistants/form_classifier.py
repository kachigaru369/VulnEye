# form_classifier.py

from bs4 import BeautifulSoup

def extract_inputs_from_html(html: str) -> list[str]:
    print("extracting the inputs from main url after login...")
    soup = BeautifulSoup(html, 'html.parser')
    input_data = []
    for field in soup.find_all(["input", "textarea", "label", "button"]):
        for attr in ["name", "placeholder", "id", "value"]:
            value = field.get(attr)
            if value:
                input_data.append(value.lower())
        if field.text:
            input_data.append(field.text.strip().lower())
    return input_data




def classify_form(inputs: list[str]) -> str:
    joined = " ".join(inputs).lower()

    if "username" in joined and "password" in joined:
        return "login"
    elif "email" in joined and "password" in joined and ("confirm" in joined or "signup" in joined):
        return "signup"
    elif "search" in joined or "query" in joined or "find" in joined:
        return "search"
    elif "comment" in joined or "message" in joined or "post" in joined:
        return "comment"
    elif "contact" in joined or "phone" in joined or "subject" in joined:
        return "contact"
    elif "upload" in joined or "file" in joined or "choosefile" in joined:
        return "upload"
    elif "ip" in joined or "host" in joined or "cmd" in joined or "command" in joined:
        return "command"
    elif "reset" in joined and "password" in joined:
        return "reset-password"
    elif "feedback" in joined or "rate" in joined or "review" in joined:
        return "feedback"
    elif "admin" in joined or "panel" in joined:
        return "admin"
    elif "id" in joined and "submit" in joined:
        return "sqli"
    else:
        return "unknown"

