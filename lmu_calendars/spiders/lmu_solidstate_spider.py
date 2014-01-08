from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from datetime import datetime, timedelta
import pytz
import re

from lmu_calendars.items import ICalendarEventItem

class LMUKolloquiumSpider(CrawlSpider):
    name = "lmu_solidstate_spider"
    allowed_domains = ['physik.uni-muenchen.de']
    start_urls = ["http://www.theorie.physik.uni-muenchen.de/lsschollwoeck/talks_seminars/solid_state_theory/index.html"]
    
    # Extract links that go to a colloquium page
    # How not to revisit links??
    rules = (
        Rule(SgmlLinkExtractor(allow=('solid_state_theory/archiv_20141/.*/index\.html$',),),
             callback = 'parse_item', follow = True),)


    def parse_start_url(self, response):
        # This method is called on the response from start_urls request and allows for parsing the parent page
        pass
       
    def parse_item(self, response):
        # This method is called on the response from each link followed
        hxs = HtmlXPathSelector(response)
        
        items = []

        # title
        title = hxs.select("//div[@class='user-html']/h1[@class='g-h1']/text()").extract()[0].strip(" \n")

        # subtitle gives speaker and affiliation
        speaker_details = hxs.select("//div[@class='titeleiste']/h3/text()").extract()[0]

        # date and time section
        date_and_time = hxs.select("//div[@class='titeleiste']/h4/text()")
        date = date_and_time.re('(\d{1,2}\.\d{1,2}\.\d{4})')[0]
        times = date_and_time.re('(\d{1,2}:\d{2})')
        start_time = times[0]
        end_time = times[1] if len(times) > 1 else None

        location = hxs.select("//div[@class='eingerueckt']/p/text()").extract()[0].strip("\n ")

        abstract_pieces = hxs.select("//div[@class='titeleiste']/p")

        abstract = []

        for para in abstract_pieces:
            text_list = para.select(".//text()").extract()

            if text_list:
                para_text = "\n\n".join([txt.strip(" \n") for txt in text_list])  
                abstract.append(para_text)
        
        abstract = "\n\n".join(abstract)
        
        # Convert date to a datetime object
        (day, mth, yr) = map(int, date.split("."))

        time_separator = ":" if ":" in start_time else "."
        germany_TZ = pytz.timezone('Europe/Berlin')

        (hr1, mn1)= map(int, start_time.split(":"))
        start_time_DT = germany_TZ.localize(datetime(yr, mth, day, hr1, mn1))

        if end_time:
            (hr2, mn2) = map(int, end_time.split(":"))
            end_time_DT = germany_TZ.localize(datetime(yr, mth, day, hr2, mn2))
        else:
            end_time_DT = start_time_DT + timedelta(hours = 1.25)

        item = ICalendarEventItem()        
        item['summary'] = u"Solid State Theory Seminar: " + title      
        item['url'] = response.url
        item['dtstart'] = start_time_DT
        item['dtend'] = end_time_DT
        item['uid'] = str(hash(str(start_time_DT.isoformat()) + title))
        item['description'] = "Speaker: " + speaker_details + "\n\n" + abstract + "\n\n" + response.url        
        item['location'] = location

        return item
