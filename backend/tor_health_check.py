import requests
import sys

def check_tor_connectivity():
    print("Checking Tor connectivity...")
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        # Use a known Tor-friendly check site
        response = requests.get('http://check.torproject.org', proxies=proxies, timeout=15)
        if "Congratulations" in response.text:
            print("✅ Tor Tunnel Verified: Connection is routed through Tor.")
            return True
        else:
            print("❌ Tor Tunnel Failed: Connection exists but is NOT routed through Tor.")
            return False
    except Exception as e:
        print(f"❌ Tor Tunnel Error: {str(e)}")
        print("\nTroubleshooting: Ensure the Tor service is running on port 9050.")
        return False

if __name__ == "__main__":
    if check_tor_connectivity():
        sys.exit(0)
    else:
        sys.exit(1)
