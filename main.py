# main.py (نسخه با پشتیبانی از Selenium)

import argparse
from core import crawler, scanner, selenium_scanner

def auto_mode(base_url):
    print(f"[+] شروع crawl آدرس: {base_url}")
    pages = crawler.crawl_site(base_url)
    print(f"[+] {len(pages)} صفحه پیدا شد. بررسی فرم‌ها و آسیب‌پذیری‌ها...\n")
    for page in pages:
        scanner.scan_page(page)

def selenium_mode(base_url):
    print(f"[+] اجرای حالت selenium روی آدرس: {base_url}")
    selenium_scanner.scan_with_browser(base_url)

def manual_mode(attack_type, target_url):
    print(f"[+] حالت دستی فعال. اجرای {attack_type} روی {target_url}\n")
    scanner.manual_attack(target_url, attack_type)

def main():
    parser = argparse.ArgumentParser(description="VulnEye - Web Vulnerability Scanner")
    parser.add_argument("--url", required=True, help="آدرس سایت هدف")
    parser.add_argument("--mode", choices=["auto", "manual", "selenium"], default="auto")
    parser.add_argument("--attack", help="نوع حمله (برای حالت manual)")
    parser.add_argument("--target", help="URL هدف برای تست (در حالت manual)")

    args = parser.parse_args()

    if args.mode == "auto":
        auto_mode(args.url)
    elif args.mode == "selenium":
        selenium_mode(args.url)
    elif args.mode == "manual":
        if not args.attack or not args.target:
            print("[!] لطفاً --attack و --target را مشخص کن")
        else:
            manual_mode(args.attack, args.target)

if __name__ == "__main__":
    main()
