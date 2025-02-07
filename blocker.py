import os
import sys
import logging
import re
from typing import List
from pathlib import Path
import argparse


class WebsiteBlocker:
    def __init__(self, hosts_file: str, redirect_ip: str = "127.0.0.1"):
        self.hosts_file = Path(hosts_file)
        self.redirect_ip = redirect_ip
        self.setup_logging()

    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("website_blocker.log"),
                logging.StreamHandler(),
            ],
        )

    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        """Validate domain name format"""
        pattern = r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
        return bool(re.match(pattern, domain))

    @staticmethod
    def is_admin() -> bool:
        """Check for administrative privileges"""
        if os.name == "nt":
            return os.system("net session >nul 2>&1") == 0
        return os.geteuid() == 0

    def validate_hosts_file(self) -> bool:
        """Validate hosts file exists and is writable"""
        try:
            if not self.hosts_file.exists():
                logging.error(f"Hosts file not found: {self.hosts_file}")
                return False
            if not os.access(self.hosts_file, os.W_OK):
                logging.error(f"No write permission for hosts file: {self.hosts_file}")
                return False
            return True
        except Exception as e:
            logging.error(f"Error validating hosts file: {e}")
            return False

    def modify_hosts_file(self, websites: List[str], action: str):
        """Modify hosts file with proper backup and validation"""
        if not self.is_admin():
            raise PermissionError("Administrative privileges required")

        if not self.validate_hosts_file():
            raise FileNotFoundError("Hosts file validation failed")

        # Validate all domains before proceeding
        invalid_domains = [site for site in websites if not self.is_valid_domain(site)]
        if invalid_domains:
            raise ValueError(f"Invalid domain names: {', '.join(invalid_domains)}")

        try:
            # Read current content
            with open(self.hosts_file, "r") as file:
                content = file.readlines()

            if action == "block":
                # Add new entries if they don't exist
                existing_entries = {line.strip() for line in content}
                new_entries = []

                for site in websites:
                    entry = f"{self.redirect_ip} {site}"
                    if entry not in existing_entries:
                        new_entries.append(f"{entry}\n")

                if new_entries:
                    with open(self.hosts_file, "a") as file:
                        file.writelines(new_entries)
                    logging.info(f"Blocked websites: {', '.join(websites)}")

            elif action == "unblock":
                # Remove entries for specified websites
                new_content = [
                    line
                    for line in content
                    if not any(site in line for site in websites)
                ]

                with open(self.hosts_file, "w") as file:
                    file.writelines(new_content)
                logging.info(f"Unblocked websites: {', '.join(websites)}")

        except Exception as e:
            logging.error(f"Error modifying hosts file: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(description="Website Access Management Tool")
    parser.add_argument(
        "action", choices=["block", "unblock"], help="Action to perform"
    )
    parser.add_argument(
        "--websites",
        "-w",
        nargs="+",
        required=True,
        help="List of websites to block/unblock",
    )
    parser.add_argument(
        "--redirect",
        "-r",
        default="127.0.0.1",
        help="IP address to redirect to (default: 127.0.0.1)",
    )

    args = parser.parse_args()

    hosts_file = (
        r"C:\Windows\System32\drivers\etc\hosts" if os.name == "nt" else "/etc/hosts"
    )

    try:
        blocker = WebsiteBlocker(hosts_file, args.redirect)
        blocker.modify_hosts_file(args.websites, args.action)
    except Exception as e:
        logging.error(f"Operation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
