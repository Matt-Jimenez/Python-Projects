# Active Directory User Audit

This script audits user accounts in an Active Directory domain using the ldap3 library【790539124674921†L186-L256】. The script searches for disabled or inactive users, moves them into security groups, or removes accounts based on criteria.

## Features

- Connects to a domain controller using ldap3【790539124674921†L186-L256】.
- Searches for user accounts based on status or attributes.
- Generates CSV reports of disabled or inactive users.
- Moves users to groups or removes them when needed.

## Prerequisites

- Python 3.8 or later.
- Access to an Active Directory domain and credentials with enough privileges.
- Install dependencies from `requirements.txt`.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Edit `main.py` to set the domain controller, base DN, and user credentials.
3. Run the script:
   ```
   python main.py
   ```
4. Review the generated report and logs.