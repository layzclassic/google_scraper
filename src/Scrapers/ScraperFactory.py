import sys
import os
sys.path.append('C:\\Users\\Ben\\Desktop\\Projects\\Rankines-SEO-Shit\\google_scraper\\src')

from bs4 import BeautifulSoup
from bs4 import Tag
from Model import *

def MakeScraper(tag : Tag):
    # HLCard - first google result with lots of links
    if 'class' in tag.parent.attrs and tag.parent.attrs['class'] == 'hlcw0c':
        #return HLCardScraper(tag)
        return None
    # People also ask card ignore
    elif len(tag.select("div.g")) == 0:
        return None
    # RegularCard - regular google result
    else:        
        return RegularCardScraper(tag)