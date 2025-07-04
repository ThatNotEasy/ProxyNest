import requests
import os
from colorama import Fore, Style, init

init(autoreset=True)

API_LIST = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=100&country=all",
    "https://cms.iproyal.com/api/free-proxy-records?fields[0]=ip&fields[1]=port&pagination[page]={page}&pagination[pageSize]=100",
    "https://proxylist.geonode.com/api/proxy-list"
]

def fetch_proxies(pages=1, output_file="proxies/fetch_proxies.txt"):
    if not os.path.exists("proxies"):
        os.makedirs("proxies")

    common_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    geo_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,ms;q=0.8,fr;q=0.7',
        'dnt': '1',
        'origin': 'https://geonode.com',
        'priority': 'u=1, i',
        'referer': 'https://geonode.com/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': common_headers['user-agent'],
    }

    auth_headers = common_headers.copy()
    auth_headers['accept'] = '*/*'
    auth_headers['accept-language'] = 'en-US,en;q=0.9'
    auth_headers['authorization'] = 'Bearer c07d9ce184008ff4be5ab6afa6a67a7513e5ece56e43b60ad1ddb0b86f952318e1ebebf54825bccb6191da8ad135cc29c963ce3f1c46dc4ad8364440333d6bee44ae20e3f0e63c29d3c5139c35f84b70d88b4e5de1e2f25cf07dca5d40fa5c0fa093490a5919e3269f2fa853776c59642c50b0cfc761c7f3943edd1908605661'

    total_fetched = 0
    with open(output_file, "a") as f:
        for api in API_LIST:
            if "iproyal" in api:
                for page in range(1, pages + 1):
                    url = api.replace("{page}", str(page))
                    try:
                        response = requests.get(url, headers=auth_headers, timeout=10)
                        response.raise_for_status()
                        data = response.json()
                        proxies = data.get("data", [])
                        for item in proxies:
                            ip = item.get("ip")
                            port = item.get("port")
                            if ip and port:
                                f.write(f"{ip}:{port}\n")
                                total_fetched += 1
                        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Page {page} from IPRoyal: {len(proxies)} proxies")
                    except Exception as e:
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} IPRoyal page {page} failed: {e}")

            elif "geonode" in api:
                for page in range(1, pages + 1):
                    try:
                        params = {
                            'limit': '100',
                            'page': str(page),
                            'sort_by': 'lastChecked',
                            'sort_type': 'desc',
                        }
                        response = requests.get(api, headers=geo_headers, params=params, timeout=10)
                        response.raise_for_status()
                        data = response.json()
                        proxies = data.get("data", [])
                        valid_count = 0
                        for item in proxies:
                            ip = item.get("ip")
                            port = item.get("port")
                            protocols = item.get("protocols", [])
                            if ip and port and protocols:
                                # You can optionally filter protocol types here, e.g. if "http" in protocols:
                                f.write(f"{ip}:{port}\n")
                                total_fetched += 1
                                valid_count += 1
                        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Page {page} from GeoNode: {valid_count} proxies")
                    except Exception as e:
                        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} GeoNode page {page} failed: {e}")

            else:
                try:
                    response = requests.get(api, timeout=10)
                    response.raise_for_status()
                    lines = response.text.strip().splitlines()
                    for line in lines:
                        if ':' in line:
                            f.write(line.strip() + "\n")
                            total_fetched += 1
                    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {len(lines)} proxies fetched from plain API")
                except Exception as e:
                    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed plain API fetch: {e}")

    print(f"\n{Fore.GREEN}[DONE]{Style.RESET_ALL} Total proxies saved: {total_fetched}")
    print(f"{Fore.YELLOW}[PATH]{Style.RESET_ALL} Output file: {output_file}")