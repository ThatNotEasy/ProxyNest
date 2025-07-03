import requests
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Shared session across requests
session = requests.Session()

def get_country(ip, session):
    """Get country of an IP address using ipapi.co."""
    try:
        response = session.get(f"https://ipapi.co/{ip}/country_name/", timeout=5)
        if response.status_code == 200 and response.text.strip() != "Undefined":
            return response.text.strip()
        return "Unknown"
    except requests.RequestException:
        return "Unknown"

def save_working_proxy(proxy, country, output_file="proxies/working_proxies.txt"):
    """Save a single working proxy to file immediately."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'a') as file:
        file.write(f"{proxy} - {country}\n")

def check_proxy(proxy, timeout=5):
    cookies = {
        'XSRF-TOKEN': 'eyJpdiI6IlFocnVtY28ycU5RSVhxMVdJNVE5bGc9PSIsInZhbHVlIjoiYVRYck9ndXpYeElWdjg0VW8rN2thUVRFZkRVcHd2TlFacG1qS3VPRE9wUmhaMzZwUjN4WWVkUDgxeHRSejNBSiIsIm1hYyI6IjJjNTFkZjU4MGE3NTg5NmFmNjkwOTQzYTcwMzhhZGE5YjUxNjE5MGNjOTAxMTBhYTU3YTZiZDYwZmNiOTZkZjAifQ%3D%3D',
        'ip_geolocation_api_session': 'eyJpdiI6ImFwTjBqNGhDbnA1OTc5SHRpbGdvamc9PSIsInZhbHVlIjoia2k0OFNKc1dReXU2eEl0djlZUkZOYUZJV2hjTk55XC96Y2FJNXJnVVJxYzgzNmpNRTF1QWV6blwvMUFlZmI3WCtFaXR3YnVjZDVxa3NMUmRhU3ZjUlgwbGhVeThUc0Rycmo0TDlDYmpTdzJ6STBJbmptTmJHY3B4cEZ4MkRyTkp6RCIsIm1hYyI6Ijc2NjMxZGE5MTU0OTA5M2VmMTA3NDcxY2NmMjQyMWMxZmI3ZDViMDZkZjY3ZjUwZjQ0ZTIyYTBiMWNhOGYwYTYifQ%3D%3D',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ms;q=0.8,fr;q=0.7',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        # 'cookie': 'XSRF-TOKEN=eyJpdiI6IlFocnVtY28ycU5RSVhxMVdJNVE5bGc9PSIsInZhbHVlIjoiYVRYck9ndXpYeElWdjg0VW8rN2thUVRFZkRVcHd2TlFacG1qS3VPRE9wUmhaMzZwUjN4WWVkUDgxeHRSejNBSiIsIm1hYyI6IjJjNTFkZjU4MGE3NTg5NmFmNjkwOTQzYTcwMzhhZGE5YjUxNjE5MGNjOTAxMTBhYTU3YTZiZDYwZmNiOTZkZjAifQ%3D%3D; ip_geolocation_api_session=eyJpdiI6ImFwTjBqNGhDbnA1OTc5SHRpbGdvamc9PSIsInZhbHVlIjoia2k0OFNKc1dReXU2eEl0djlZUkZOYUZJV2hjTk55XC96Y2FJNXJnVVJxYzgzNmpNRTF1QWV6blwvMUFlZmI3WCtFaXR3YnVjZDVxa3NMUmRhU3ZjUlgwbGhVeThUc0Rycmo0TDlDYmpTdzJ6STBJbmptTmJHY3B4cEZ4MkRyTkp6RCIsIm1hYyI6Ijc2NjMxZGE5MTU0OTA5M2VmMTA3NDcxY2NmMjQyMWMxZmI3ZDViMDZkZjY3ZjUwZjQ0ZTIyYTBiMWNhOGYwYTYifQ%3D%3D',
    }
    ip, _ = proxy.split(":")
    test_url = "https://api.ipify.org/"

    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }

    try:
        response = session.get(test_url, proxies=proxies, cookies=cookies, headers=headers, timeout=timeout)
        if response.status_code == 200:
            country = get_country(ip, session)
            print(f"{Fore.GREEN}[WORKING]{Style.RESET_ALL} {proxy} (Country: {country})")
            save_working_proxy(proxy, country)
            return {"proxy": proxy, "country": country}
    except (requests.RequestException, ValueError):
        print(f"{Fore.RED}[FAILED]{Style.RESET_ALL} {proxy}")
        return None

def load_proxies(file_path):
    """Load proxies from a file."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} File not found: {file_path}")
        return []
