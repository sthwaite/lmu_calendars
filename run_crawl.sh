#!/bin/bash

#
# Simple bash driver to launch spiders that generate .ics files for LMU seminars
#
# Copyright Simon Thwaite, January 2014 
# simon.thwaite@gmail.com

SCRAPY=/project/theorie/s/Simon.Thwaite/libraries/scrapy-scrapy-a19c880/bin/scrapy
CRAWL_DIR=/project/theorie/s/Simon.Thwaite/work/lmu_calendars
FEED_DIR=/project/theorie/s/Simon.Thwaite/work/lmu_calendars/ics

cd $CRAWL_DIR

rm -f $FEED_DIR/LMU_MPK_calendar.ics
$SCRAPY crawl lmu_mpk_spider --set FEED_URI=$FEED_DIR/LMU_MPK_calendar.ics --set FEED_FORMAT=ics

rm -f $FEED_DIR/LMU_ASC_calendar.ics
$SCRAPY crawl lmu_asc_spider --set FEED_URI=$FEED_DIR/LMU_ASC_calendar.ics --set FEED_FORMAT=ics

rm -f $FEED_DIR/LMU_physikmodern_calendar.ics
$SCRAPY crawl lmu_physikmodern_spider --set FEED_URI=$FEED_DIR/LMU_physikmodern_calendar.ics --set FEED_FORMAT=ics

rm -f $FEED_DIR/LMU_CeNS_calendar.ics
$SCRAPY crawl lmu_cens_spider --set FEED_URI=$FEED_DIR/LMU_CeNS_calendar.ics --set FEED_FORMAT=ics

rm -f $FEED_DIR/LMU_solidstate_calendar.ics
$SCRAPY crawl lmu_solidstate_spider --set FEED_URI=$FEED_DIR/LMU_solidstate_calendar.ics --set FEED_FORMAT=ics

date > $FEED_DIR/last_updated.dat

# Local commit all modified files and push db to remote master on GitHub
git commit -a -m "Calendars current as of ""`date`"
git push origin master