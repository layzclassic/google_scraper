from .CardScraper import CardScraper
from bs4 import Tag

class RegularCardScraper(CardScraper):
    def __init__(self, tag : Tag):        
        super().__init__(tag)
    
    def Scrape(self):
        if self.tag == None:
            return
        
        results = self.tag.select("div.kvH3mc")

        for result in results:
            self.ScrapeDetails(result)

        if len(results) == 0:
            self.ScrapeDetails(self.tag)