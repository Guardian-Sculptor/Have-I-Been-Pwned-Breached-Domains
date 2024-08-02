import requests
import json
import time
import datetime
import csv
from config import HIBP_headers, HIBP_LINK

def export_to_csv(data,domain,writer):
    for email_id, values in data.items():
        email_address= email_id + "@" + domain
        writer.writerow([email_address, ', '.join(values)])

def HIBP_call(domain,writer):
    response = requests.get(f"{HIBP_LINK}{domain}", headers=HIBP_headers)
    if response.status_code == 200:
        data = response.json()
        export_to_csv(data,domain,writer)
    else:
        print(f"Error on {domain}: {response.status_code}")

def read_domains():
    domains = []
    with open('Domains.txt', 'r') as file:
        for line in file:
          domains.append(line.strip())
    return domains

def Filename_with_date():
    today = datetime.date.today()
    formatted_date = today.strftime("%B_%d_%Y")
    filename = f"{formatted_date}_hibp.csv"
    return filename

if __name__ == "__main__":
    domains=read_domains()
    filename = Filename_with_date()
    
    csvfile = open(filename, 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(['Username', 'Breaches'])
    
    for domain in domains:
        HIBP_call(domain,writer)
        print(domain + " completed")
        time.sleep(5)
