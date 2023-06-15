#chromedriver_path = r'C:\Users\suen6\PycharmProjects\google_scraper\file\chromedriver'  # update this path
import re
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

chromedriver_path = r'C:\Users\suen6\PycharmProjects\google_scraper\file\chromedriver'  # update this path

class Website:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.email = self.find_emails()

    def find_emails(self):
        emails = self.scrape_emails(self.url)
        contact_page_link = self.find_contact_us_page(self.url)
        if contact_page_link:
            emails.extend(self.scrape_emails(contact_page_link))
        return emails

    @staticmethod
    def find_contact_us_page(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        anchors = soup.find_all('a')
        for anchor in anchors:
            if 'contact' in anchor.text.lower():
                contact_page_link = anchor.get('href')
                if contact_page_link.startswith('/'):
                    contact_page_link = url + contact_page_link
                return contact_page_link
        return None

    @staticmethod
    def scrape_emails(url):
        response = requests.get(url)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        emails = re.findall(email_pattern, response.text)
        return emails

def scrape_google_search(query):
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}&num=100"
    webdriver_service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=webdriver_service)
    driver.get(URL)
    results = driver.find_elements(By.CSS_SELECTOR, '.g .tF2Cxc')
    websites = []
    for result in results:
        title = result.find_element(By.CSS_SELECTOR, '.LC20lb.DKV0Md').text
        url = result.find_element(By.CSS_SELECTOR, '.yuRUbf a').get_attribute('href')
        website = Website(title, url)
        websites.append(website)
    driver.quit()
    return websites

def save_to_csv(websites, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Title', 'URL', 'Emails']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for website in websites:
            writer.writerow({'Title': website.title, 'URL': website.url, 'Emails': ", ".join(website.email)})

if __name__ == '__main__':
    query = 'your google search query'  # replace with your search query
    websites = scrape_google_search(query)
    save_to_csv(websites, 'output.csv')

