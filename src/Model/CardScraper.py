from .Website import Website
from bs4 import Tag

class CardScraper:
    def __init__(self, tag : Tag):
        self.tag = tag
        self.websites = []

    def Scrape(self):
        return
        #print("Base")

    def ScrapeDetails(self, subTag):
        website = Website()

        # title
        title_element = subTag.select_one("h3.LC20lb.DKV0Md")
        if title_element:
            website.title = title_element.text
        # Scrape URL
        url_element = subTag.select_one("a")
        if url_element and "href" in url_element.attrs:
            website.url = url_element["href"]
        # Scrape domain
        domain_element = subTag.select_one("div.apx8Vc.qLRx3b.tjvcx.GvPZzd.cHaqb")
        if domain_element:
            website.domain = domain_element.text
        # Scrape description
        description_element = subTag.select_one(".VwiC3b.MUxGbd")
        if description_element:
            website.description = description_element.text

        self.websites.append(website)