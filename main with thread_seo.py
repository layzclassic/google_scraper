from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
import time

def scrape_web(query):
    query = query.replace(' ', '+')
    url = f"https://google.com/search?q={query}&num=13"
    print("Scraping URL:", url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    }
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        print('Soup completed')
    else:
        print('Error: Failed to retrieve search results')
        return []

    results = []
    for div in soup.find_all('div', class_='SC7lYd'):
        title_element = div.find('div', class_='LC20lb MBeuO DKV0Md')
        title = title_element.text if title_element else ''

        description_div = div.find('div', class_='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc')
        descriptions = [span.text for span in description_div.find_all('span')] if description_div else []

        url_element = div.find('cite', class_='apx8Vc qLRx3b tjvcx GvPZzd cHaqb')
        url = url_element.text if url_element else ''

        date_span = div.find('span', class_='MUxGbd wuQ4Ob WZ8Tjf')
        date = date_span.find('span').text if date_span and date_span.find('span') else ''

        item = {
            "title": title,
            "descriptions": descriptions,
            "url": url,
            "date": date
        }
        results.append(item)

    for row in results:
        print(row)
    return results

def save(websites):
    data = []
    for item in websites:
        data.append({
            'title': item.get('title', ''),
            'url': item.get('url', ''),
            'description': item.get('description', ''),
            'date': item.get('date', '')
        })

    header = ['title', 'url', 'description','date']
    df = pd.DataFrame(data, columns=header)
    file_path = r'C:\Users\t490s\Documents\GitHub\google_scraper\export_list'
    base_name = 'hong kong'
    file_name = base_name + '.csv'
    counter = 1
    while os.path.exists(os.path.join(file_path, file_name)):
        file_name = base_name + str(counter) + '.csv'
        counter += 1
    file_pathname = os.path.join(file_path, file_name)
    df.to_csv(file_pathname, index=False)
    print("Emails saved to:", file_pathname)


def main(query):
    print("Starting web scraping...")
    websites = scrape_web(query)
    save(websites)
    print("Web scraping completed.")


if __name__ == '__main__':
    query = '"eSIM travel" AND "america"'
    main(query)
