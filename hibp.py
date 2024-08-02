import requests
import json
import time
import datetime
import csv
from config import HIBP_headers, HIBP_Breached_Domains_Link, HIBP_Subscribed_Domains_Link

def export_to_csv(data,domain,writer):
    for email_id, values in data.items():
        email_address= email_id + "@" + domain
        writer.writerow([email_address, ', '.join(values)])


def HIBP_call(domain,writer):
    response = requests.get(f"{HIBP_Breached_Domains_Link}{domain}", headers=HIBP_headers)
    if response.status_code == 200:
        data = response.json()
        export_to_csv(data,domain,writer)
    else:
        print(f"Error on {domain}: {response.status_code}")

def get_domains():
    domains = []
    response = requests.get(f"{HIBP_Subscribed_Domains_Link}", headers=HIBP_headers)
    if response.status_code == 200:
        data = response.json()
        for line in data:
            domains.append(line['DomainName'].strip())
    return domains

def Filename_with_date():
    today = datetime.date.today()
    formatted_date = today.strftime("%B_%d_%Y")
    filename = f"{formatted_date}_hibp.csv"
    return filename

if __name__ == "__main__":
    domains=get_domains()
    print(domains)
    filename = Filename_with_date()
    
    csvfile = open(filename, 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(['Username', 'Breaches'])
    
    for domain in domains:
        HIBP_call(domain,writer)
        print(domain + " completed")
        time.sleep(5)
