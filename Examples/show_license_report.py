import logging
import os

import urllib3
from ucmdb_rest import UCMDBServer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Use Case:  Display the license report
"""

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("license_report")

def main():
    script_dir = os.path.dirname(__file__)
    cred_path = os.path.join(script_dir,'credentials.json')
    client = UCMDBServer.from_json(cred_path)

    try:
        logger.info(f"Generating License Audit for {client.server}...\n")
        response = client.system.getLicenseReport()
        data = response.json()

        used = float(data.get('usedUnit', 0))
        total = float(data.get('totalLicenseUnit', 0))
        days_left = data.get('remainingDays', 'N/A')

        print("=" * 50)
        print(f"{'UCMDB LICENSE EXECUTIVE SUMMARY':^50}")
        print("=" * 50)
        print(f"License Units Used:   {used:>10}")
        print(f"Total Capacity:       {total:>10}")
        print(f"Days Until Expiry:    {days_left:>10}")
        
        if used > total:
            print(f"\n*** WARNING: LICENSE OVER-CONSUMPTION BY {round(used - total, 2)} UNITS ***")
        print("=" * 50)

        types = ['Server', 'Workstation', 'Network', 'Storage', 'Docker']

        print(f"\n{'Unit Type':<20} | {'Full':<10} | {'Basic':<10}")
        print("-" * 50)

        for t in types:
            f_val = data.get(f'full{t}Count', 0)
            b_val = data.get(f'basic{t}Count', 0)
            print(f"{t:<20} | {f_val:<10} | {b_val:<10}")

        if 'licenseDetailsCollection' in data:
            print("\n" + "=" * 50)
            print(f"{'INSTALLED LICENSE KEYS':^50}")
            print("=" * 50)
            for lic in data['licenseDetailsCollection']:
                print(f"Description: {lic.get('description')}")
                print(f"Capacity:    {lic.get('capacity')} Units")
                print(f"Expires:     {lic.get('formatExpirationDate')}")
                print("-" * 50)

    except Exception as e:
        logger.error(f"Failed to generate license report: {e}")

if __name__ == "__main__":
    main()