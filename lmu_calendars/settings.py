# Scrapy settings for lmu_calendars project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'lmu_calendars'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['lmu_calendars.spiders']
NEWSPIDER_MODULE = 'lmu_calendars.spiders'
DEFAULT_ITEM_CLASS = 'lmu_calendars.items.ICalendarEventItem'
USER_AGENT = '{0:s} {1:s}'.format(BOT_NAME, BOT_VERSION)

FEED_EXPORTERS = {'ics': 'lmu_calendars.exporters.ICalendarExporter'}
