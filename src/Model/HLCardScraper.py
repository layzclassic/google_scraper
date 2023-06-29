from .CardScraper import CardScraper
from .HLSmallCardScraper import HLSmallCardScraper
from bs4 import Tag

class HLCardScraper(CardScraper):
    def __init__(self, tag : Tag):
        super().__init__(tag)
    
    def Scrape(self):
        if self.tag == None:
            return
                
        bigOne = self.tag.select_one("div.tF2Cxc")
        if bigOne:
            self.ScrapeDetails(bigOne)

        table = self.tag.select_one("table.jmjoTe")
        if table:
            rows = self.table.select("td")

            for row in rows:
                smallScraper = HLSmallCardScraper(row)
                smallScraper.Scrape()

                for website in smallScraper.websites:
                    self.websites.append(website)
