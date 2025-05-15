# test_form_classifier.py

from form_classifier import classify_form

def test_forms():
    forms = {
        "Login Form": ["username", "password", "submit"],
        "Search Form": ["search", "go", "query"],
        "Comment Box": ["your comment", "message", "name"],
        "Signup Form": ["email", "password", "confirm"],
        "Contact Us": ["phone", "email", "contact", "message"],
        "Unknown": ["title", "content", "send"]
    }

    for label, fields in forms.items():
        result = classify_form(fields)
        print(f"{label:15} => {result}")

if __name__ == "__main__":
    test_forms()
