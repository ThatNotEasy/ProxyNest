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

## 🤝 Contributing

Contributions are welcome! If you have improvements, new proxy sources, or better validation methods, feel free to open a PR or submit an issue.

---

## ✨ Stay Anonymous & Happy Scraping!
