import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

class Website:
    def __init__(self, title=None, url=None, domain=None, byline_date=None, description=None, sitelinks=None, rich_attributes=None):
        self.title = title
        self.url = url
        self.domain = domain
        self.byline_date = byline_date
        self.description = description
        self.sitelinks = sitelinks
        self.rich_attributes = rich_attributes

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

    # Scrape websites
    website_results = soup.select("div.kvH3mc.BToiNc.UK95Uc, div.BYM4Nd")
    for website_result in website_results:
        website_data = {}

        if website_result.has_attr("class") and "kvH3mc" in website_result["class"]:
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

        if website_result.has_attr("class") and "BYM4Nd" in website_result["class"]:
            # Scrape title
            title_element = website_result.select_one("h3 a")
            if title_element:
                website_data["title"] = title_element.text

            # Scrape URL
            url_element = website_result.select_one("h3 a")
            if url_element and "href" in url_element.attrs:
                website_data["url"] = url_element["href"]

            # Scrape description
            description_element = website_result.select_one("div.zz3gNc")
            if description_element:
                website_data["description"] = description_element.text

            # Scrape sitelinks
            sitelinks_element = website_result.select("div.usJj9c")
            if sitelinks_element:
                sitelinks = []
                for sitelink_element in sitelinks_element:
                    sitelink = {}

                    # Scrape title
                    title = sitelink_element.select_one("h3")
                    if title:
                        sitelink["title"] = title.text

                    # Scrape URL
                    url = sitelink_element.select_one("h3 a")
                    if url and "href" in url.attrs:
                        sitelink["url"] = url["href"]

                    # Scrape description
                    description = sitelink_element.select_one("div.zz3gNc")
                    if description:
                        sitelink["description"] = description.text

                    sitelinks.append(sitelink)

                website_data["sitelinks"] = sitelinks

        results["websites"].append(Website(**website_data))

    return results


from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd

def save_to_xlsx(data, base_name, file_path):
    workbook = Workbook()

    # Create a separate worksheet for each class
    for class_name, class_data in data.items():
        worksheet = workbook.create_sheet(title=class_name)
        worksheet.append(["Type", "Title", "URL", "Domain", "Byline Date", "Description", "Sitelinks", "Rich Attributes"])

        if class_name == "websites":
            for website in class_data:
                sitelinks = pd.DataFrame(website.sitelinks) if website.sitelinks else pd.DataFrame()
                rich_attributes = pd.DataFrame(website.rich_attributes) if website.rich_attributes else pd.DataFrame()

                # Append each row of the sitelinks dataframe
                for row in dataframe_to_rows(sitelinks, index=False, header=False):
                    worksheet.append(["Website", website.title, website.url, website.domain, website.byline_date, website.description, *row, ""])

                # Append each row of the rich attributes dataframe
                for row in dataframe_to_rows(rich_attributes, index=False, header=False):
                    worksheet.append(["", "", "", "", "", "", "", *row])

    # Remove the default sheet created and save the workbook
    workbook.remove(workbook["Sheet"])
    workbook.save(file_path)

# Example usage
query = "textrapp"
num_results = 15
data = scrape_google_search(query, num_results)
base_name = "google_search_results"
file_path = "file.xlsx"
save_to_xlsx(data, base_name, file_path)
