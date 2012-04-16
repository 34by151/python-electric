#!/usr/bin/env python

import sys
import getopt
import settings
import datetime
import MySQLdb
import logging, logging.handlers, logging.config
from dbop import TED_DBOP, RunningAveragesDBOP
from charts import CreateDayDetailChart

logging.config.fileConfig(settings.LOG.CONFIGFILE)
log = logging.getLogger("python_electric.data_processor")

class Data_Processor ():
    def __init__(self):
        try:
            log.info ("Connecting to database %s", settings.DATABASE.NAME)
            self.db = MySQLdb.connect(user=settings.DATABASE.USER , passwd=settings.DATABASE.PASSWORD, db=settings.DATABASE.NAME)
        except MySQLdb.Error, e:
            log.critical ("Error %s: %s", e.args[0], e.args[1])
            sys.exit ("Error %d: %s" % (e.args[0], e.args[1]))
        
    def CreateSecondChart (self, date):
        log.debug ("Data_Processor.CreateSecondChart")
        start = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        end = datetime.datetime(date.year, date.month, date.day, 23, 59, 59)
        MTU = 0
        table = settings.DATABASE.TABLES['second']
        log.debug("CreateSecondChart: Using table %s", table)
        # Look up db table
        db_history = TED_DBOP (self.db, table)
        history = db_history.GetHistory (MTU, start, end)
        # if nothing in history, exit function
        if history == None: return None
        
        unzipped = zip (*history)
        CreateDayDetailChart(start,unzipped[2],unzipped[3])

    def daterange(self, start_date, end_date):
        log.debug ("Data_Processor.daterange")
        for n in range((end_date - start_date).days):
            yield start_date + datetime.timedelta(n)

    def UpdateSecondCharts (self):
        log.debug ("Data_Processor.UpdateSecondsCharts")
        MTU = 0
        table = settings.DATABASE.TABLES['second']
        log.debug("UpdatingSecondsChart: Reading table %s", table)
            
        # Look up db table
        db_history = TED_DBOP (self.db, table)

        # get last date entry date in table
        db_history_min = db_history.GetMinDate(MTU)
        db_history_max = db_history.GetMaxDate(MTU)
        
        #db_history_min = datetime.datetime(2010,7,13,0,0,0)
        #print db_history_min, db_history_max
        
        for date in self.daterange(db_history_min, db_history_max):
            log.debug("UpdatingSecondsChart: Creating chart for %s", date)
            CreateSecondChart(date)

    def UpdateRunningAverage (self):
        log.debug ("Data_Processor.UpdateRunningAverage")
        MTU = 0
        table = settings.DATABASE.TABLES['day']
        log.debug("CreateRunningAverage: Updating table %s", table)
            
        # Look up db table
        db_history = TED_DBOP (self.db, table)
        db_averages = RunningAveragesDBOP (self.db, "electric_average_day")

        # get last date entry date in table
        db_history_datetime = db_history.GetMaxDate(MTU)
        db_averages_datetime = db_averages.GetMaxDate(MTU)

        log.debug("CreateRunningAverage: db_history_datetime: %s, db_history_datetime: %s",  db_history_datetime, db_history_datetime)
            
        if db_averages_datetime == None:
            # No DB entries... get all second history data from TED:
            history = db_history.GetHistory (MTU)
            
            s = {} 
            average = {} 
            data = []
        
            for i in range (0, len(history)):
                end = i
                
                for y in [7, 14, 21, 28]:
                    s[y] = end-y+1

                    sum = 0
                    count = 0
                    average[y] = 0
                    
                    if s[y] >= 0:
                        for x in range(s[y], end+1):
                            sum += history[x][3]
                            count += 1
                        average[y] = round(sum/count, 3)
                
                data.append([MTU, history[end][2], average[7], average[14], average[21], average[28]])
            
            # insert history data in DB...
            db_averages.InsertData (data)

        elif db_history_datetime > db_averages_datetime:
            d = db_history_datetime - db_averages_datetime 

            log.debug("RunningAverage: Difference between history and average is %s days", d.days)

            history = db_history.GetHistory (MTU, db_averages_datetime - datetime.timedelta(days=28))

            s = {} 
            average = {} 
            data = []
        
            for i in range (0, len(history)):
                end = i

                if history[i][2] <= db_averages_datetime: continue
                
                for y in [7, 14, 21, 28]:
                    s[y] = end-y+1

                    sum = 0
                    count = 0
                    average[y] = 0
                    
                    if s[y] >= 0:
                        for x in range(s[y], end+1):
                            sum += history[x][3]
                            count += 1
                        average[y] = round(sum/count, 3)
                
                data.append([MTU, history[end][2], average[7], average[14], average[21], average[28]])
            
            # insert history data in DB...
            db_averages.InsertData (data)

        elif db_history_datetime <= db_averages_datetime:
            log.info("RunningAverage: DB electric_average_day (%s) is equal or greater than TED_history_second datetime (%s)!  DB not updated.", db_averages_datetime, db_history_datetime)
        
    

if __name__=="__main__":
##    main(sys.argv[1:])

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdrsyao:", 
        ["help", "updaterunningavg", "updatedetail", "updatedetaillast",
         "updatedetailall", "updatedetailone="])
    except getopt.GetoptError:          
        ##usage()                         
        print "Arguments not valid... show usage"
        sys.exit(2)
    
    _debug = False
    _running = False
    _detail = False
    _detaillast = False
    _detailall = False
    _detailone = False
    _detaildate = None
                 
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            ##usage()                     
            sys.exit()                  
        elif opt == '-d':              
            _debug = True
        elif opt in ("-r", "--updaterunningavg"):
            # will update running average chart
            _running = True
        elif opt in ("-s", "--updatedetail"):
            # will update today's detail chart
            _detail = True
        elif opt in ("-y", "--updatedetaillast"):
            # will update yesterday's detail chart
            _detaillast = True
        elif opt in ("-a", "--updatedetailall"):
            # will update all detail charts
            _detailall = True
        elif opt in ("-o", "--updatedetailone"):
            # will update specefied detail chart
            _detailone = True
            _detaildate = arg    
            
  
    log.debug("Running...")

    processor = Data_Processor()
    
    now = datetime.datetime.now()
    
    
    if _running:
        log.debug("updating running average")
        processor.UpdateRunningAverage()
    if _detail:
        log.debug("updating second now")
        processor.CreateSecondChart(now)
    if _detaillast:
        log.debug("updating second last")
        processor.CreateSecondChart(now-datetime.timedelta(days=1))
    if _detailall:
        log.debug("updating second all")
        processor.UpdateSecondCharts()
    if _detailone:
        log.debug("updating second one")
##        if _detaildate is date:
##            CreateSecondChart(_detaildate)
        


