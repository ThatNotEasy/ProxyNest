import argparse
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from modules.banners import banners
from modules.checker import CHECKER
from modules.api import API
from colorama import Fore, Style

checker = CHECKER()
api = API()

def process_proxy(args):
    proxy, protocol = args
    try:
        result = checker.check_proxy(proxy, protocol)
        if result:
            proxy, proto, country = result
            print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Protocol: {proto.upper()}, Country: {country}")
            checker.save_working_proxy(proxy, country)
            return (proxy, proto, country)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to check {proxy}: {str(e)}")
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Proxy Fetcher & Checker - Collect and test HTTP/HTTPS/SOCKS proxies.",
        epilog=(
            "Examples:\n"
            "  python main.py -f proxies.txt           # Check proxies (sequentially)\n"
            "  python main.py -f proxies.txt -t 50     # Check proxies with 50 threads\n"
            "  python main.py -c 5                     # Fetch proxies from API (5 pages = ~500 proxies)"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("-f", "--file", type=str, help="Check proxies from file (e.g., proxies.txt)")
    parser.add_argument("-c", "--count", type=int, help="Fetch proxies from API (each page returns 100 proxies)")
    parser.add_argument("-t", "--thread", type=int, help="Use threading with number of worker threads")
    parser.add_argument("-p", "--protocol", type=str, choices=["http", "https", "socks4", "socks5"], help="Specify protocol to test (default: all protocols)")

    args = parser.parse_args()

    try:
        if args.file:
            proxies = checker.load_proxies(args.file)
            if not proxies:
                print("No proxies found to check.")
                return

            print(f"Checking {len(proxies)} proxies {'with ' + str(args.thread) + ' threads' if args.thread else 'sequentially'}...\n")
            start_time = time.time()

            if args.thread:
                working_proxies = []
                with ThreadPoolExecutor(max_workers=args.thread) as executor:
                    futures = {executor.submit(process_proxy, proxy): proxy for proxy in proxies}
                    for future in as_completed(futures):
                        result = future.result()
                        if result:
                            working_proxies.append(result)
            else:
                working_proxies = []
                for proxy in proxies:
                    result = process_proxy(proxy)
                    if result:
                        working_proxies.append(result)

            end_time = time.time()
            print(f"\nCheck completed in {end_time - start_time:.2f} seconds")
            print(f"Found {len(working_proxies)} working proxies out of {len(proxies)}")

        elif args.count:
            print(f"Fetching {args.count} page(s) of proxies from API...\n")
            api.fetch_proxies(args.count)

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n\n[Interrupted] Operation cancelled by user.")
        sys.exit(0)

if __name__ == "__main__":
    banners()
    main()
