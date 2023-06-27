import requests
from bs4 import BeautifulSoup
import pandas as pd
from Model.Website import Website

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

    try:
        # Scrape websites
        website_results = soup.select("div.MjjYud div.g")
        for website_result in website_results:
            website_data = {}

            # Check if brand display is present
            brand_display_element = website_result.find_previous_sibling("div", class_="hlcw0c")
            brand_display = bool(brand_display_element)

            website_data["brand_display"] = brand_display

            # Scrape title
            title_element = website_result.select_one("h3.LC20lb.DKV0Md")
            if title_element:
                website_data["title"] = title_element.text

            # Scrape URL
            url_element = website_result.select_one("a")
            if url_element and "href" in url_element.attrs:
                website_data["url"] = url_element["href"]

            # Scrape domain
            domain_element = website_result.select_one("div.apx8Vc.qLRx3b.tjvcx.GvPZzd.cHaqb")
            if domain_element:
                website_data["domain"] = domain_element.text

            # Scrape description
            description_element = website_result.select_one(".VwiC3b.MUxGbd")
            if description_element:
                website_data["description"] = description_element.text

            # Scrape sitelinks
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

            website = Website(**website_data)
            results["websites"].append(website)
            print("Scraped:", website.__dict__)
    except Exception as e:
        print(f"Error occurred during web scraping: {str(e)}")

    return results