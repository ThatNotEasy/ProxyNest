# 🕸️ ProxyNest

**ProxyNest** is a fast, modular Python toolkit for fetching, validating, and managing free HTTP/HTTPS proxies. 🧰  
Whether you're scraping the web, anonymizing traffic, or building a proxy pool, ProxyNest helps you discover and manage working proxies with ease.

---

## 🚀 Features

- 🔍 **Fetch Proxies**: Scrape proxies from public proxy listing APIs or websites.
- ⚡ **High-Speed Validation**: Multi-threaded proxy checker for fast, parallel testing.
- 🌍 **Geo & Protocol Filtering**: Organize working proxies by country, anonymity level, or protocol (HTTP/HTTPS).
- 💾 **Save & Load**: Persist working proxies to disk in TXT.

---

## 📸 Screenshots

### 🔄 Fetching Proxies
![Fetching Proxies](https://github.com/user-attachments/assets/a47af9af-cdcd-480b-a35b-7c359f9d81fb)

---

### ✅ Checking Proxies (Multi-threaded)
![Checking Proxies](https://github.com/user-attachments/assets/77ef518b-2e72-48a4-95ac-e3ea8bf7babd)

---

## 🛠️ Installation

```bash
git clone https://github.com/ThatNotEasy/ProxyNest.git
cd proxynest
pip install -r requirements.txt
```

---

## ⚙️ Usage

### 🧲 Fetch Proxies
```bash
python main.py -c <count>
```

### 🔎 Check Proxies (W/O Thread)
```bash
python main.py -f <proxies>
python main.py -f <proxies> -t <thread>
```

### 📁 Output
Working proxies are saved to:
- `working_proxies.txt`

---

## 🤝 Contributing

Contributions are welcome! If you have improvements, new proxy sources, or better validation methods, feel free to open a PR or submit an issue.

---

## ✨ Stay Anonymous & Happy Scraping!
