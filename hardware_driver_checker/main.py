"""
Hardware and driver checker.

Queries Windows Management Instrumentation (WMI) to list devices and driver versions and compares them against an approved list.
"""

import json
import wmi

APPROVED_FILE = 'approved_versions.json'
OUTPUT_FILE = 'driver_report.csv'


def load_approved():
    """Load approved driver versions from a JSON file."""
    try:
        with open(APPROVED_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def check_drivers():
    """Compare installed driver versions with approved versions and write a report."""
    approved = load_approved()
    c = wmi.WMI()
    report = []
    for driver in c.Win32_PnPSignedDriver():
        name = driver.DeviceName
        version = driver.DriverVersion
        status = 'OK'
        if name in approved and approved[name] != version:
            status = 'Update Required'
        report.append([name, version, status])
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('Device,Version,Status\n')
        for row in report:
            f.write(','.join(row) + '\n')


if __name__ == '__main__':
    check_drivers()