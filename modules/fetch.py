import requests
import os
from colorama import Fore, Style, init

init(autoreset=True)

API_LIST = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&simplified=true",
    "https://cms.iproyal.com/api/free-proxy-records?fields[0]=ip&fields[1]=port&pagination[page]={page}&pagination[pageSize]=100"
]

def fetch_proxies(pages=1, output_file="proxies/fetch_proxies.txt"):
    if not os.path.exists("proxies"):
        os.makedirs("proxies")

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'Bearer c07d9ce184008ff4be5ab6afa6a67a7513e5ece56e43b60ad1ddb0b86f952318e1ebebf54825bccb6191da8ad135cc29c963ce3f1c46dc4ad8364440333d6bee44ae20e3f0e63c29d3c5139c35f84b70d88b4e5de1e2f25cf07dca5d40fa5c0fa093490a5919e3269f2fa853776c59642c50b0cfc761c7f3943edd1908605661',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    total_fetched = 0
    with open(output_file, "a") as f:
        for api in API_LIST:
            # print(f"{Fore.BLUE}[SOURCE]{Style.RESET_ALL} {api}")
            if "iproyal" in api:
                # Handle iproyal paginated API
                for page in range(1, pages + 1):
                    url = api.replace("{page}", str(page))
                    try:
                        response = requests.get(url, headers=headers, timeout=10)
                        response.raise_for_status()
                        data = response.json()
                        proxies = data.get("data", [])
                        for item in proxies:
                            ip = item.get("ip")
                            port = item.get("port")
                            if ip and port:
                                f.write(f"{ip}:{port}\n")
                                total_fetched += 1
                        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Page {page} fetched: {len(proxies)} proxies")
                    except Exception as e:
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed page {page}: {e}")
            else:
                # Handle plain text APIs like ProxyScrape
                try:
                    response = requests.get(api, timeout=10)
                    response.raise_for_status()
                    lines = response.text.strip().splitlines()
                    for line in lines:
                        if ':' in line:
                            f.write(line.strip() + "\n")
                            total_fetched += 1
                    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {len(lines)} proxies fetched")
                except Exception as e:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to fetch: {e}")

    print(f"\n{Fore.GREEN}[DONE]{Style.RESET_ALL} Total proxies saved: {total_fetched}")
    print(f"{Fore.YELLOW}[PATH]{Style.RESET_ALL} Output file: {output_file}")