import requests
import json
import time
import datetime
import csv
import os
HIBP_HEADERS = {'hibp-api-key': os.environ['HIBP_API_KEY'] }

def export_to_csv(data,domain,writer):
    for email_id, values in data.items():
        email_address= email_id + "@" + domain
        writer.writerow([email_address, ', '.join(values)])

def HIBP_call(domain,writer):
    response = requests.get(f"{os.environ['HIBP_BREACHED_DOMAINS_LINK']}{domain}", headers=HIBP_HEADERS)
    while True :
        if response.status_code == 200:
            data = response.json()
            export_to_csv(data,domain,writer)
            break
        elif response.status_code == 429:
            retry_time = response.headers.get('retry-after', 5)
            print("sleep requested for" + retry_time )
            time.sleep(retry_time + 1)
            
        else:
            print(f"Error on {domain}: {response.status_code}")
            print(response.text)
            break

def get_domains():
    domains = []
    response = requests.get(os.environ['HIBP_SUBSCRIBED_DOMAINS_LINK'], headers=HIBP_headers)
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
    filename = Filename_with_date()
    
    csvfile = open(filename, 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(['Username', 'Breaches'])
    
    for domain in domains:
        HIBP_call(domain,writer)
        print(domain + " completed")
        
