import os
import sys

HOSTS_FILE = (
    r"C:\Windows\System32\drivers\etc\hosts" if os.name == "nt" else "/etc/hosts"
)

REDIRECT_IP = "127.0.0.1"

BLOCKED_SITES = ["www.facebook.com", "facebook.com", "www.youtube.com", "youtube.com"]


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
