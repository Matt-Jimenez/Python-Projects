"""
Active Directory user audit script.

This script connects to an Active Directory domain controller using ldap3 and produces a report of disabled accounts.
"""

import os
import csv
from ldap3 import Server, Connection, ALL, SUBTREE

# Configuration values can be provided via environment variables or edited here.
DOMAIN_CONTROLLER = os.getenv("AD_SERVER", "ldap://ad.example.com")
USERNAME = os.getenv("AD_USER", "cn=admin,dc=example,dc=com")
PASSWORD = os.getenv("AD_PASSWORD", "password")
BASE_DN = os.getenv("AD_BASE_DN", "dc=example,dc=com")


def audit_users():
    """Connect to the domain controller and write a CSV of disabled users."""
    server = Server(DOMAIN_CONTROLLER, get_info=ALL)
    conn = Connection(server, user=USERNAME, password=PASSWORD, auto_bind=True)
    # Search for disabled accounts using the userAccountControl bit mask.
    conn.search(
        search_base=BASE_DN,
        search_filter="(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))",
        search_scope=SUBTREE,
        attributes=["distinguishedName", "sAMAccountName"],
    )
    # Write results to CSV
    with open("disabled_users.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["distinguishedName", "sAMAccountName"])
        for entry in conn.entries:
            writer.writerow([
                entry.distinguishedName.value,
                entry.sAMAccountName.value,
            ])
    conn.unbind()


if __name__ == "__main__":
    audit_users()