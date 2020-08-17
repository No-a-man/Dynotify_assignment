from selectorlib import Extractor
import requests 
import json 
from time import sleep


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('markd.yml')

def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading"+url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page "+url+" was blocked by Amazon. Please try using better proxies\n")
        else:
            print("Page "+url+" must have been blocked by Amazon as the status code was"+ str(r.statuscode))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)

# product_data = []
x=input("Enter what u have to search")
url="https://www.amazon.com/s?k="+str(x)
with open('sungoutput.jsonl','w') as outfile:
    
    data = scrape(url) 
    if data:
        for product in data['products']:
            product['search_url'] = url
            print("Saving Product: %s"%product['title'])
            json.dump(product,outfile)
            outfile.write("\n")
            # sleep(5)