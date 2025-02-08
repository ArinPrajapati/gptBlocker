import os
import sys
import logging

HOSTS_FILE = (
    r"C:\Windows\System32\drivers\etc\hosts" if os.name == "nt" else "/etc/hosts"
)

REDIRECT_IP = "139.59.195.30" ## static IP address of the server where the website is hosted

BLOCKED_SITES = ["www.facebook.com", "facebook.com"]

# Configure logging
logging.basicConfig(
    filename='web_blocker.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_admin():
    """Check if script is running with admin/root privileges"""
    if os.name == "nt":
        return os.system("net session >nul 2>&1") == 0
    else:
        return os.geteuid() == 0


def block_websites():
    """Block websites by adding them to the hosts file"""
    if not is_admin():
        print("[!] Please run the script as Administrator or Root.")
        sys.exit(1)

    with open(HOSTS_FILE, "r+") as file:
        content = file.read()

        for site in BLOCKED_SITES:
            entry = f"{REDIRECT_IP} {site}\n"
            if entry not in content:
                file.write(entry)
                logging.info(f"Blocked {site}")

    print("[✅] Websites blocked successfully!")


def unblock_websites():
    """Unblock websites by removing them from the hosts file"""
    if not is_admin():
        print("[!] Please run the script as Administrator or Root.")
        sys.exit(1)

    with open(HOSTS_FILE, "r") as file:
        lines = file.readlines()

    with open(HOSTS_FILE, "w") as file:
        for line in lines:
            if not any(site in line for site in BLOCKED_SITES):
                file.write(line)
            else:
                logging.info(f"Unblocked {line.strip()}")

    print("[✅] Websites unblocked successfully!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py [block | unblock]")
        sys.exit(1)

    if sys.argv[1] == "block":
        block_websites()
    elif sys.argv[1] == "unblock":
        unblock_websites()
    else:
        print("Invalid argument. Use 'block' or 'unblock'.")
