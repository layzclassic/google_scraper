import sys
sys.path.append('C:/Users/Ben/Desktop/Projects/Rankines-SEO-Shit/google_scraper/src')

import Helpers.ExcelWriter as ExcelWriter
import Helpers.ConfigReader as ConfigReader
from Scrapers.GoogleScraper import scrape_google_search

# Example usage
config = ConfigReader.ReadConfig()
data = scrape_google_search(config.get('Main', 'query'), config.get('Main', 'num_results'))
ExcelWriter.save_to_xlsx(data, config.get('Main', 'basename'), config.get('Main', 'filepath'))