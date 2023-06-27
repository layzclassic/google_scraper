import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd

from openpyxl.styles import Font

class Website:
    def __init__(self, title=None, url=None, domain=None, byline_date=None, description=None, sitelinks=None, rich_attributes=None, brand_display=None):
        self.title = title
        self.url = url
        self.domain = domain
        self.byline_date = byline_date
        self.description = description
        self.sitelinks = sitelinks
        self.rich_attributes = rich_attributes
        self.brand_display = brand_display


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

def save_to_xlsx(data, base_name, file_path):
    workbook = Workbook()

    # Create a separate worksheet for each class
    for class_name, class_data in data.items():
        worksheet = workbook.create_sheet(title=class_name)
        worksheet.append(["Type", "Title", "URL", "Domain", "Byline Date", "Description", "Sitelinks", "Rich Attributes", "Brand Display"])

        if class_name == "websites":
            for website in class_data:
                sitelinks = website.sitelinks if website.sitelinks else {}
                rich_attributes = website.rich_attributes if website.rich_attributes else {}

                # Append the main website row
                worksheet.append(["Website", website.title, website.url, website.domain, website.byline_date, website.description, "", "", website.brand_display])

                # Append each sitelink row
                for i in range(max(len(sitelinks.get("questions", [])), len(sitelinks.get("answers", [])), len(sitelinks.get("dates", [])))):
                    question = sitelinks.get("questions", [""])[i] if sitelinks.get("questions") else ""
                    answer = sitelinks.get("answers", [""])[i] if sitelinks.get("answers") else ""
                    date = sitelinks.get("dates", [""])[i] if sitelinks.get("dates") else ""
                    worksheet.append(["", "", "", "", "", "", question, answer, ""])

                # Append each rich attribute row
                for attribute, value in rich_attributes.items():
                    worksheet.append(["", "", "", "", "", "", "", attribute, value])

    # Remove the default sheet created and save the workbook
    workbook.remove(workbook["Sheet"])
    workbook.save(file_path)

# Example usage
query = "esim"
num_results = 15
data = scrape_google_search(query, num_results)
base_name = "google_search_results"
file_path = "file.xlsx"
save_to_xlsx(data, base_name, file_path)
