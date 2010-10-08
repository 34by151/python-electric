from data_processor import Data_Processor
from data_import import UpdateTEDDB
import datetime
import settings
import logging, logging.config
from dbop import RunningAveragesDBOP
import MySQLdb
import os, time

logging.config.fileConfig(settings.LOG.CONFIGFILE)
log = logging.getLogger("python_electric.iterator")

now = datetime.datetime.now() + datetime.timedelta(hours=-7)
midnight = datetime.datetime(now.year, now.month, now.day)
yesterday = midnight - datetime.timedelta(days=1)

# update database (runs every time)
log.info('---- updating TED Database from TED 5000')
UpdateTEDDB()

# creates new or updates current second chart, should run every time
log.info('---- updating/creating current second chart')
processor = Data_Processor()
processor.CreateSecondChart(now)

# no need to check if db is up to date, processor.UpdateRunningAverage function logs warning if up to date.
log.info('---- Updating Running Average database' )
processor.UpdateRunningAverage()

# update yesterdays second chart if after midnight
file = settings.CHART.PATH + yesterday.strftime('%Y%m%d.png')

#                                       Sat Sep 11 13:45:32 2010
modified = datetime.datetime.strptime(time.ctime(os.path.getmtime(file)), '%a %b %d %H:%M:%S %Y')

if modified < (midnight-datetime.timedelta(minutes=10)):
    log.info("---- Updating yesterday's second chart. %s (file date = %s)", file, modified)
    processor.CreateSecondChart(now-datetime.timedelta(days=1))
else:
    log.info("---- Yesterday's second chart already up to date. %s (file date = %s)", file, modified  )



    
