

## 🔐 **VulnEye – Web Vulnerability Scanner CLI**

**VulnEye** is a modular, interactive command-line tool designed for penetration testers and cybersecurity students to analyze and exploit common web vulnerabilities in a streamlined and automated fashion.

The current version supports **Command Injection**, with more modules being actively developed to cover a wide spectrum of web security flaws.

---

### 🚀 **How to Use**

1. **Launch the CLI interface**:

```bash
python3 VulnEye.py
```

2. **Select the vulnerability scanner** from the menu:

   * `[1] Command Injection`
   * (Other options will appear as modules are added)

3. **Follow prompts**:

   * Provide the target URL
   * Authenticate if needed
   * The tool automatically detects input fields and attempts payload injection

---

### 📦 **Features**

* 🔎 **Automatic form field detection**
* 🔐 **Login handling & session management**
* 🧠 **Dynamic payload injection engine**
* 📄 **Modular design (easy to expand)**

---

### 🧪 **Planned Modules (Coming Soon)**

> VulnEye is expanding to support the following vulnerabilities:

* 🛡️ **CSRF** *(Cross-Site Request Forgery)*
* 🗂️ **File Inclusion** *(LFI/RFI detection)*
* ⬆️ **File Upload** *(insecure upload points)*
* ❌ **Insecure CAPTCHA** *(bypassable CAPTCHA checks)*
* 💉 **SQL Injection**
* 👻 **Blind SQL Injection**
* 🔑 **Weak Session IDs**
* 🧬 **XSS (DOM-Based)**
* 💥 **XSS (Reflected)**
* 🧠 **XSS (Stored/Persistent)**
* 🔓 **CSP Bypass** *(Content Security Policy evasion)*
* 📜 **JavaScript Security Flaws**
* 🚪 **Authorisation Bypass**
* 🔀 **Open HTTP Redirects**
* 🔐 **Cryptographic Misuse**
* ⚙️ **API Vulnerabilities**

---

### 📁 Project Structure (Modular)

```bash
VulnEye/
├── VulnEye.py               # Main CLI launcher
├── CommandInjection.py      # Command Injection module
├── SqlInjection.py          # Upcoming SQLi module
├── XssScanner.py            # Upcoming XSS module
├── html_field_finder.py     # Handles form parsing
├── RedirectionScanner.py    # Handles login/session/redirects
├── requirements.txt         # Dependencies
```

---

### ✅ Best Use Case

Ideal for:

* Red team exercises
* Web CTF practice
* Testing local vulnerable apps (e.g., DVWA, BWAPP, WebGoat)
* Building your own custom modules

---

