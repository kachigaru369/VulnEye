#!/usr/bin/env python3

import sys , os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "core")))
from pyfiglet import figlet_format
from colorama import init, Fore, Style
import CommandInjection

# import SqlInjection
# import XssScanner

init(autoreset=True)

# def show_poster():
#     try:
#         with open("poster.txt", "r", encoding="utf-8") as f:
#             print(Fore.LIGHTWHITE_EX + f.read())
#     except FileNotFoundError:
#         print(Fore.RED + "[!] poster.txt not found.")

def show_banner():
    print(Fore.CYAN + figlet_format("VulnEye", font="big"))  # ← smaller font
    print(Fore.YELLOW + "Web Vulnerability Scanner")
    print(Fore.MAGENTA + "Created by Kachigaru - 2025\n")

def main_menu():
    try:
        while True:
            print(Fore.GREEN + """
[1] Command Injection
[2] SQL Injection (Coming Soon)
[3] XSS (Coming Soon)
[0] Exit
""")
            choice = input(Fore.CYAN + "Select an option: ").strip()

            if choice == "1":
                CommandInjection.starter()
            elif choice == "2":
                print(Fore.YELLOW + "[!] SQL Injection scanner is under development.")
            elif choice == "3":
                print(Fore.YELLOW + "[!] XSS scanner is under development.")
            elif choice == "0":
                print(Fore.CYAN + "Goodbye!")
                sys.exit(0)
            else:
                print(Fore.RED + "[!] Invalid option. Please enter a number between 0 and 3.\n")
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Interrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"[X] Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # show_poster()
    show_banner()
    main_menu()
