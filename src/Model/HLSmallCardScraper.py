from bs4 import Tag
import Model
from .Website import Website

class HLSmallCardScraper(Model.HLCardScraper):
    def __init__(self, tag : Tag):        
        super().__init__(tag)
    
    def Scrape(self):
        if self.tag != None:
            
            website = Website()

            subTag = self.tag

            # title
            title_element = subTag.select_one("a.l")
            if title_element:
                website.title = title_element.text

            # Scrape URL
            url_element = subTag.select_one("a.l")
            if url_element and "href" in url_element.attrs:
                website.url = url_element["href"]
           
            # Scrape description
            description_element = subTag.select_one("div.zz3gNc")
            if description_element:
                website.description = description_element.text

            self.websites.append(website)