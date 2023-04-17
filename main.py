#Import libraries

from bs4 import BeautifulSoup
import urllib
import requests
import re
from re import search
import pandas as pd
from urllib.parse import urlsplit
from collections import deque

def scrape_web(query):
    # Build search query and URL to scrape
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}&num=100"
    print(URL)

    # define desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    # Parse the HTML with Beautiful soup
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        print('soup complete')

    # Strip links and titles from HTML and append to a list

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
                "link": link
            }
            results.append(item)

    for row in urls_list:
        print(row)

def scrape():
    ## scraping - the fun part
    new_email_count = 0
    scraped = set()
    unscraped = []
    emails = set()
    urls_list1 = ['https://thredboskiaccommodation.com.au/']

    for x in urls_list1:
        url = x
        # break each URL apart
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path:
            path = url[:url.rfind('/') + 1]
        else:
            path = url
        print("Crawling URL %s" % url)

        # start crawling the URL
        timeout = time.time() + 60
        while time.time() < timeout:
            try:
                response = requests.get(url)  # response is the returned html of each url
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.(?:com|au)", response.text,
                                    re.I))  # extract email from the URL itself

        if len(new_emails) == 1:  # if there are not contact emails on that page, then look for a contact page
            print('email found', new_emails)
        else:
            print('no email found, checking for contacts page')
            soup = BeautifulSoup(response.text, 'lxml')

            contact_link = soup.find("a", href=True,
                                     text=re.compile('.*contact.*|.*enquir.*|.*get in touch.*', flags=re.IGNORECASE))
            if contact_link is None:
                print('no contact page found')
                print('\n #--------------')
            else:
                contact_link = contact_link['href']
                if re.search(r'.*#.*', contact_link, re.I):
                    print('this link is shit')
                    contact_link = float("NaN")
                elif contact_link.startswith('/'):
                    contact_link = base_url + contact_link

                # elif not x.startswith('http'):
                #   contact_link_href = path + contact_link_href

                print('checking contact page:', contact_link)

            try:
                response = requests.get(contact_link)  # response is the returned html of each url
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.(?:com|au)", response.text,
                                        re.I))  # extract email from the URL itself
            if new_emails != 0:
                new_email_count += 1
                print('email found:', new_emails)
        emails.update(new_emails)
        print('\n #--------------')

        # for anchor in soup.find_all("a"):
        #   if 'contact' in anchor:
        #     print(anchor)

        #     if "href" in anchor.attrs:
        #       link = anchor.attrs["href"]
        #     else:
        #       link = ''

        # if not link.endswith(".gz"):
        #   if not link in unscraped and not link in scraped:
        #       unscraped.append(link)

    # df = pd.DataFrame(emails, columns=["Email"])
    # df.to_csv('email.csv', index=False)

    # files.download("email.csv")


def main(query):
    website = scrape_web(query)
    scrape(website)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    query = 'lol'
    main(query)


