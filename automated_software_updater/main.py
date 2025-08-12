"""
Automated software updater.

Detects the operating system and updates packages to desired versions. Reads desired versions from a JSON file and logs the updates.
"""

import json
import platform
import subprocess

DESIRED_FILE = 'desired_versions.json'
LOG_FILE = 'update.log'


def load_desired():
    """Load desired package versions from JSON."""
    try:
        with open(DESIRED_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def update_windows(desired):
    """Run updates on Windows using winget."""
    for package, version in desired.items():
        cmd = ['winget', 'upgrade', package, '--version', version, '--silent']
        subprocess.run(cmd)
        with open(LOG_FILE, 'a', encoding='utf-8') as log:
            log.write(f'Updated {package} to {version}\n')


def update_linux(desired):
    """Run updates on Linux using apt-get."""
    for package, version in desired.items():
        cmd = ['sudo', 'apt-get', 'install', '-y', f'{package}={version}']
        subprocess.run(cmd)
        with open(LOG_FILE, 'a', encoding='utf-8') as log:
            log.write(f'Installed {package} {version}\n')


def main():
    desired = load_desired()
    system = platform.system()
    if system == 'Windows':
        update_windows(desired)
    else:
        update_linux(desired)


if __name__ == '__main__':
    main()