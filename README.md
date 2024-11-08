# PPTP Brute-force Tool

`pptp_bruteforce.py` is a Python tool designed to attempt brute-force attacks against a PPTP (Point-to-Point Tunneling Protocol) VPN server. By providing a username, wordlist, and other configurable options, this script allows multiple password attempts to be made in parallel.

> **Warning**: This tool is intended for educational purposes and authorized penetration testing only. Unauthorized usage is illegal. Always obtain explicit permission before using it on any system.

## Features
- Brute-force password attempts against PPTP VPN servers.
- Customizable username, port, and number of parallel attempts (threads).
- Default username of `administrator` if not specified.
- Verbose mode for detailed debugging and output.
- Automatic termination of attempts upon finding a successful password.

## Requirements
- **Python 3.x**: This script is compatible with Python 3.x.
- **Sudo privileges**: The script uses `pppd` via `sudo`, which requires elevated permissions.
- **pppd with pptp.so plugin**: `pppd` and `pptp.so` (for PPTP) must be installed.

## Installation
Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/pptp_bruteforce.git
cd pptp_bruteforce
```

## Usage

### Command-line Arguments
`python3 pptp_bruteforce.py <server_ip> -w <wordlist_file> [-u <username>] [-p <port>] [-t <threads>] [-v]`

### Arguments
- `<server_ip>`: IP address of the PPTP VPN server (positional argument, required).
- `-u`, `--user`: Username for the PPTP server. Default: `administrator`.
- `-w`, `--wordlist`: Path to the password wordlist file (required).
- `-p`, `--port`: PPTP server port. Default: `1723`.
- `-t`, `--threads`: Number of concurrent threads for parallel attempts. Default: `1`.
- `-v`, `--verbose`: Enable verbose mode for detailed debugging output.

### Examples
1. **Basic Usage** (default username `administrator`, single-threaded):
   `sudo python3 pptp_bruteforce.py 81.149.238.57 -w wordlist.txt`

2. **Custom Username, Port, and Multiple Threads**:
   `sudo python3 pptp_bruteforce.py 81.149.238.57 -u user01 -w wordlist.txt -p 1723 -t 5`

3. **Verbose Mode for Debugging**:
   `sudo python3 pptp_bruteforce.py 81.149.238.57 -w wordlist.txt -v`

## How It Works
1. **Load Wordlist**: Reads the provided wordlist file and attempts each password.
2. **Parallel Processing**: Uses Python's `ThreadPoolExecutor` to handle concurrent password attempts based on the specified thread count.
3. **Early Exit on Success**: The script stops all attempts if a valid password is found, printing the successful password.
4. **Verbose Mode**: When `-v` is enabled, the script provides detailed output at each stage, including debugging information for each password attempt and command execution.

## Notes
- **Sudo Privileges**: Running `pppd` requires root access, so `sudo` is necessary.
- **Rate Limiting**: Excessive thread usage may impact both local and remote system performance.
- **Ensure Permissions**: Unauthorized use of brute-force techniques is illegal and punishable by law.

## Troubleshooting
- **Missing `pptp.so`**: Ensure the PPTP client package is installed on your system.
- **Permission Denied**: If you encounter permission issues, try running the script with `sudo`.
- **Firewall or Network Blocks**: Make sure the PPTP server is accessible and that there are no firewall or network restrictions preventing connection attempts.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

**Warning**: Only use this tool on systems where you have explicit permission for penetration testing.

---

**Contributors**: Created by [Your Name](https://github.com/conorarmstrong)
