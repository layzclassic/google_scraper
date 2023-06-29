import requests
from bs4 import BeautifulSoup
import pandas as pd
from .ScraperFactory import MakeScraper

def scrape_google_search(query, num_results):
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    results = {
        "websites": []
    }

    #try:
    if True:
        # Scrape websites
        website_results = soup.select("div.MjjYud")
        for website_result in website_results:
            scraper = MakeScraper(website_result)

            if scraper == None:
                continue

            scraper.Scrape()

            website_data = {}

            # Check if brand display is present
            #brand_display_element = website_result.find_previous_sibling("div", class_="hlcw0c")
            #brand_display = bool(brand_display_element)

            #website_data["brand_display"] = brand_display

            
            # Scrape sitelinks
            """
            sitelinks_element = website_result.select_one(".z2IOkd")
            if sitelinks_element:
                sitelinks = {}

                questions = sitelinks_element.select("a span")
                answers = sitelinks_element.select(".e24Kjd")
                dates = sitelinks_element.select(".f.nsa.fwzPFf")

                sitelinks["questions"] = [question.text for question in questions]
                sitelinks["answers"] = [answer.text for answer in answers]
                sitelinks["dates"] = [date.text for date in dates]

                website_data["sitelinks"] = sitelinks
            """

            #website = Website(**website_data)
            for website in scraper.websites:
                results["websites"].append(website)
            #print("Scraped:", website.__dict__)
    #except Exception as e:
    #    print(f"Error occurred during web scraping: {str(e)}")

    return results