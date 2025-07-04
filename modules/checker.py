import requests
import os
import socks
from colorama import Fore, Style, init

init(autoreset=True)

class CHECKER:
    def __init__(self, timeout=10):
        self.session = requests.Session()
        self.timeout = timeout

    def get_country(self, ip):
        """Get country of an IP address using ipapi.co (strips port if present)."""
        try:
            ip_only = ip.split(":")[0]
            response = self.session.get(f"https://ipapi.co/{ip_only}/country/", timeout=self.timeout)
            if response.status_code == 200 and response.text.strip() != "Undefined":
                return response.text.strip()
            return "Unknown"
        except requests.RequestException:
            return "Unknown"

    def save_working_proxy(self, proxy, country, output_file="proxies/working_proxies.txt"):
        """Save a single working proxy to file immediately."""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        # Check for duplicates before saving
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                existing = f.read()
                if proxy in existing:
                    return False
        
        with open(output_file, 'a') as file:
            file.write(f"{proxy} - {country}\n")
        return True

    def check_proxy(self, proxy, selected_protocol=None):
        """Check if a proxy is working with specified or all supported protocols."""
        ip = proxy.split("@")[-1].split(":")[0]
        test_url = "https://api.ipify.org/"
        protocols = [selected_protocol] if selected_protocol else ["http", "socks4", "socks5"]
        country = self.get_country(ip)

        for proto in protocols:
            proxy_url = f"{proto}://{proxy}"
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }

            try:
                response = self.session.get(
                    test_url,
                    proxies=proxies,
                    timeout=self.timeout,
                    headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
                    }
                )
                if response.status_code == 200:
                    print(f"{Fore.GREEN}[WORKING]:{Fore.WHITE}{proxy} {Fore.RED}|{Fore.GREEN}{proto.upper()} {Fore.RED}| {Fore.GREEN}{country}{Style.RESET_ALL}")
                    return (proxy, proto, country)
            except (requests.RequestException, ValueError) as e:
                print(f"{Fore.RED}[FAILED]:{Fore.WHITE}{proxy}{Style.RESET_ALL}")
        return None

    def load_proxies(self, file_path):
        """Load proxies from a file, removing duplicates and empty lines."""
        try:
            with open(file_path, "r") as f:
                proxies = set()
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        proxies.add(line)
                return list(proxies)
        except FileNotFoundError:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} File not found: {file_path}")
            return []