import argparse
import time
import concurrent.futures
import sys
from modules.banners import banners
from modules.checker import load_proxies, check_proxy, save_working_proxy
from modules.fetch import fetch_proxies

def main():
    parser = argparse.ArgumentParser(
        description="Proxy Fetcher & Checker - Collect and test HTTP/HTTPS proxies.",
        epilog=(
            "Examples:\n"
            "  python main.py -f proxies.txt           # Check proxies (no threading)\n"
            "  python main.py -f proxies.txt -t 100    # Check proxies with 100 threads\n"
            "  python main.py -c 5                     # Fetch proxies from API (5 pages = ~500 proxies)"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-f", "--file", type=str,
        help="Check proxies from file (e.g., proxies.txt)"
    )
    parser.add_argument(
        "-c", "--count", type=int,
        help="Fetch proxies from API (each page returns 100 proxies)"
    )
    parser.add_argument(
        "-t", "--thread", type=int,
        help="Use multi-threading with specified number of threads"
    )

    args = parser.parse_args()

    try:
        if args.file:
            proxies = load_proxies(args.file)
            if not proxies:
                print("No proxies found to check.")
                return

            print(f"Checking {len(proxies)} proxies...")
            start_time = time.time()
            working_proxies = []

            if args.thread:
                print(f"Using threading with {args.thread} thread(s)\n")
                with concurrent.futures.ThreadPoolExecutor(max_workers=args.thread) as executor:
                    future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
                    for future in concurrent.futures.as_completed(future_to_proxy):
                        result = future.result()
                        if result:
                            working_proxies.append(result)
            else:
                for proxy in proxies:
                    result = check_proxy(proxy)
                    if result:
                        working_proxies.append(result)

            if working_proxies:
                save_working_proxy(working_proxies)

            end_time = time.time()
            print(f"\nCheck completed in {end_time - start_time:.2f} seconds")
            print(f"Found {len(working_proxies)} working proxies out of {len(proxies)}")

        elif args.count:
            print(f"Fetching {args.count} page(s) of proxies from API...")
            print()
            fetch_proxies(args.count)

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n\n[Interrupted] Operation cancelled by user.")
        sys.exit(0)

if __name__ == "__main__":
    banners()
    main()