import requests
from bs4 import BeautifulSoup
import csv
from openpyxl import Workbook

class Website:
    def __init__(self, title, url):
        self.title = title
        self.url = url

class PeopleAlsoLike:
    def __init__(self, title):
        self.title = title

class RelatedSearches:
    def __init__(self, title):
        self.title = title

def scrape_google_search(query, num_results):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    results = {
        "websites": []
    }

    # Scrape websites
    website_results = soup.select(".g")
    for website_result in website_results[:num_results]:
        website_data = {}

        # Scrape title
        title_element = website_result.select_one("h3.LC20lb.MBeuO.DKV0Md")
        if title_element:
            print('title found')
            website_data["title"] = title_element.text

        # Scrape URL
        url_element = website_result.select_one("a")
        if url_element and "href" in url_element.attrs:
            website_data["url"] = url_element["href"]

        # Scrape domain
        domain_element = website_result.select_one("div.apx8Vc.qLRx3b.tjvcx.GvPZzd.cHaqb")
        if domain_element:
            website_data["domain"] = domain_element.get_text(strip=True)

        # Scrape description
        description_element = website_result.select_one("div.VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc.lEBKkf")
        if description_element:
            spans = description_element.select("span")
            if len(spans) >= 2:
                website_data["description"] = spans[1].text
            elif len(spans) == 1:
                website_data["description"] = spans[0].text

        # Scrape sitelinks
        sitelinks_element = website_result.select_one("div.VNLkW")
        if sitelinks_element:
            sitelinks = {}
            questions = sitelinks_element.select("a.fl")
            answers = sitelinks_element.select("div.wrBvFf.OSrXXb:first-child span")
            dates = sitelinks_element.select("div.wrBvFf.OSrXXb:nth-child(2) span")

            sitelinks["questions"] = [question["href"] for question in questions]
            sitelinks["answers"] = [answer.text for answer in answers]
            sitelinks["dates"] = [date.text for date in dates]

            website_data["sitelinks"] = sitelinks

        # Scrape rich attributes
        rich_attributes_element = website_result.select_one("div.fG8Fp.uo4vr")
        if rich_attributes_element:
            rich_attributes = []
            spans = rich_attributes_element.select("span")
            aria_label = rich_attributes_element.select_one("span.z3HNkc")

            rich_attributes = [span.text for span in spans]
            if aria_label:
                rich_attributes.append(aria_label["aria-label"])

            website_data["rich_attributes"] = rich_attributes

        # Scrape byline date
        byline_date_element = website_result.select_one("span.MUxGbd.wuQ4Ob.WZ8Tjf")
        if byline_date_element:
            website_data["byline_date"] = byline_date_element.text

        results["websites"].append(Website(**website_data))

    return results

def save_to_xlsx(data, base_name, file_path):
    workbook = Workbook()

    # Create a separate worksheet for each class
    for class_name, class_data in data.items():
        worksheet = workbook.create_sheet(title=class_name)
        worksheet.append(["Type", "Title", "URL", "Domain", "Byline Date", "Description", "Sitelinks", "Rich Attributes"])

        if class_name == "websites":
            for website in class_data:
                worksheet.append(["Website", website.title, website.url, website.domain, website.byline_date, website.description, website.sitelinks, website.rich_attributes])

    # Remove the default sheet created and save the workbook
    workbook.remove(workbook["Sheet"])
    workbook.save(file_path)

# Example usage
query = "scraping tools"
num_results = 5
data = scrape_google_search(query, num_results)
base_name = "google_search_results"
file_path = r"C:\Users\suen6\PycharmProjects\google_scraper\export_list\file.xlsx"
save_to_xlsx(data, base_name, file_path)

