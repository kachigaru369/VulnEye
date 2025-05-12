# core/crawler.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited = set()

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc != ""

def crawl_site(base_url, max_depth=2):
    to_visit = [(base_url, 0)]
    found_pages = []

    while to_visit:
        current_url, depth = to_visit.pop(0)
        if current_url in visited or depth > max_depth:
            continue
        visited.add(current_url)

        try:
            response = requests.get(current_url, timeout=5)
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                continue

            print(f"[crawler] بررسی: {current_url}")
            found_pages.append(current_url)

            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                if not href:
                    continue
                joined_url = urljoin(current_url, href)
                if is_valid_url(joined_url) and urlparse(joined_url).netloc == urlparse(base_url).netloc:
                    to_visit.append((joined_url, depth + 1))

        except Exception as e:
            print(f"[crawler] خطا در بررسی {current_url}: {e}")

    return found_pages
