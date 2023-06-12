import concurrent.futures
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time

def scrape_web(query):
    query = query.replace(' ', '+')
    url = f"https://google.com/search?q={query}&num=100"
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
    urls_list = []
    for g in soup.find_all('div', class_='yuRUbf'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            urls_list.append(link)
            title = g.find('h3').text
            item = {
                "title": title,
                "url": link
            }
            results.append(item)

    for row in results:
        print(row)
    return results

def scrape_url(url):
    try:
        response = requests.get(url)
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.(?:com|au)", response.text, re.I))
        response.close()  # Close the response to release the connection

        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string
        return {'title': title, 'url': url, 'emails': new_emails}

    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        return {'title': '', 'url': url, 'emails': set()}

def scrape(websites):
    print("Scraping URLs for emails...")
    start_time = time.time()
    total_urls = len(websites)
    processed_urls = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(scrape_url, websites)

    emails = set()
    for result in results:
        emails.update(result['emails'])
        processed_urls += 1

        elapsed_time = time.time() - start_time
        avg_time_per_url = elapsed_time / processed_urls if processed_urls > 0 else 0
        remaining_urls = total_urls - processed_urls
        remaining_time = remaining_urls * avg_time_per_url

        print(f"Processed {processed_urls}/{total_urls} URLs. Estimated remaining time: {remaining_time:.2f} seconds")

    return emails

def save(emails):
    data = []
    for email in emails:
        data.append({
            'title': email['title'],
            'url': email['url'],
            'email': email['email']
        })

    header = ['title', 'url', 'email']
    df = pd.DataFrame(data, columns=header)  # Create DataFrame with specified columns
    file_path = r'C:\Users\suen6\PycharmProjects\google-scraper\export_list'
    base_name = 'textr'
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
    websites = [item['url'] for item in scrape_web(query)]
    emails = scrape(websites)
    save(emails)
    print("Web scraping completed.")

if __name__ == '__main__':
    query = 'textrapp'
    main(query)
