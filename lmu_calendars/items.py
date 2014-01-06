# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ICalendarEventItem(Item):
    
    dtstamp = Field()
    uid = Field()
    dtstart = Field()
    _class = Field()
    created = Field()
    description = Field()
    geo = Field()
    last_mod = Field()
    location = Field()
    organizer = Field()
    priority = Field()
    seq = Field()
    status = Field()
    summary = Field()
    transp = Field()
    url = Field()
    recurid = Field()
    rrule = Field()
    dtend = Field()
    duration = Field()
    attach = Field
    attendee = Field()
    categories = Field()
    comment = Field()
    contact = Field()
    exdate = Field()
    rstatus = Field()
    related = Field()
    resources = Field()
    rdate = Field()
