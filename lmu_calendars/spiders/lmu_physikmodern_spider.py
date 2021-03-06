from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from datetime import datetime, timedelta
import pytz
import re

from lmu_calendars.items import ICalendarEventItem

class LMUKolloquiumSpider(CrawlSpider):
    name = "lmu_physikmodern_spider"
    allowed_domains = ['physik.uni-muenchen.de']
    start_urls = ["http://www.physik.uni-muenchen.de/aus_der_fakultaet/kolloquien/physik_modern/index.html"]
    
    # Extract links that go to a colloquium page
    rules = (
        Rule(SgmlLinkExtractor(allow=('physik_modern/.*/index\.html$',), deny = ('/archiv_.*',) ),
             callback = 'parse_item', follow = True),)

    def parse_start_url(self, response):
        # This method is called on the response from start_urls request and allows for parsing the parent page
        pass
       
    def parse_item(self, response):
        # This method is called on the response from each link followed
        hxs = HtmlXPathSelector(response)
        
        items = []

        # title
        title = hxs.select("//h1[@class='g-h1 g-margin-bottom titel']/text()").extract()[0].strip(" \n")

        # subtitle gives speaker and affiliation
        speaker_details = hxs.select("//h2[@class='g-h3 g-no-margin-top untertitel']/text()").extract()[0]
#        affiliation_MO = re.search("(\(.*\))", speaker_details)

#        if affiliation_MO:
#            affiliation = affiliation_MO.groups(0)[0][1:-1]
#            speaker = speaker_details[ :affiliation_MO.start()]
#        else:
#            affiliation = None
#            speaker = speaker_details

        # date and time section
        date_and_time = hxs.select("//div[@class='g-box g-padding-text g-margin-top g-margin-bottom-s']/p[1]/text()")
        date = date_and_time.re('(\d{1,2}\.\d{1,2}\.\d{4})')[0]
        times = date_and_time.re('(\d{1,2}:\d{2})')
        start_time = times[0]
        end_time = times[1] if len(times) > 1 else None

        location = hxs.select("//div[@class='g-box g-padding-text g-margin-top g-margin-bottom-s']/p[2]/text()").extract()[0].strip("\n ")
        abstract = hxs.select("//div[@class='user-html hauptinhalt']/p[1]/text()").extract()[0].strip("\n ")
        # The MPK page has no extra [p] tag in the hauptinhalt. In case Physik Modern adopts this, then the following should work:
#        if not abstract:
#            abstract = hxs.select("//div[@class='user-html hauptinhalt']/text()").extract()[0].strip("\n ")           

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
        item['summary'] = u"Physik Modern: " + title      
        item['url'] = response.url
        item['dtstart'] = start_time_DT
        item['dtend'] = end_time_DT
        item['uid'] = str(hash(str(start_time_DT.isoformat()) + title))
        item['description'] = "Speaker: " + speaker_details + "\n\n" + abstract + "\n\n" + response.url        
        item['location'] = location

        return item
