#!/usr/bin/env python

"""
 This is a Python module for The Energy Detective: A low-cost whole
 house energy monitoring system. For more information on TED5000, see:

   http://theenergydetective.com

 This module was not created by Energy, Inc. nor is it supported by
 them in any way. 

 I have only tested this module with the TED5000 Gateway using the published
 xml API.  More information on the API can be found here:

   http://www.theenergydetective.com/media/TED5000-API-R330.pdf

 The most recent version of this module can be obtained at:

   http://code.google.com/p/python-electric/

 Copyright (c) 2010 Ricardo Camba <spaceriqui@gmail.com>
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
"""

import settings
from datetime import datetime, timedelta
import MySQLdb
from TED import Gateway
from dbop import TED_DBOP
import sys

import logging, logging.config

logging.config.fileConfig(settings.LOG.CONFIGFILE)
log = logging.getLogger("python_electric.data_import")

base_table = {'second': 1,
              'minute': 60,
              'hour'  : 60*60,
              'day'   : 60*60*24,
              'month' : 60*60*24*30,
             }


def UpdateTEDDB ():
    # Initialize TED Object
    TED = Gateway ()

    # create db connection:
    try:
        db = MySQLdb.connect(user=settings.DATABASE.USER , 
                passwd=settings.DATABASE.PASSWORD, db=settings.DATABASE.NAME)
    except MySQLdb.Error, e:
        log.critical ("Error %s: %s", e.args[0], e.args[1])
        sys.exit ("Error %d: %s" % (e.args[0], e.args[1]))

    for key in settings.DATABASE.TABLES.keys():
        
        table = settings.DATABASE.TABLES[key]
        base = base_table[key]
        
        log.info("UpdateTEDDB: Updating table %s from url", table)
        
        # Look up db table
        db_history = TED_DBOP (db, table)

        # get last record available from TED...
        MTU = 0
        TED_datetime = TED.GetLastHistoryDate (key, MTU)
        
        if TED_datetime == None:
            log.warning("UpdateTEDDB: No history found... skipping.")
            continue

        # get last date entry date in table
        DB_datetime = db_history.GetMaxDate(MTU)

        log.info("UpdateDB: Current TED time: %s, Last DB entry: %s", 
                        TED_datetime, DB_datetime)

        if DB_datetime == None:
            # No DB entries... get all second history data from TED:
            history = TED.GetHistory (key, MTU, 3600) 
            
            # insert history data in DB...
            db_history.InsertData (history)

        elif TED_datetime > DB_datetime:
            d = TED_datetime - DB_datetime   
            
            
            s = d.days * 24 * 60 * 60 + d.seconds
            log.info("""UpdateDB: Difference between TED and DB is %s, or %s days and %s seconds for a total of %s seconds""",
                        d, d.days, d.seconds, s)
            
            s = (s + settings.TED.IMPORT_OVERLAP * base) / base
            s = int(round(s,0))

            # get second history data from TED:
            history = TED.GetHistory (key, MTU, s) 
            
            # trim history to only dates and times needed
            i = 0
            while 1:
##                (MTU, DATE, POWER, COST, VOLTAGE, VMIN, VMAX,
##                  PMIN, PMAX, CMIN, CMAX) = history[i]
                date = history[i][1]
                if date <= DB_datetime:
                    log.info("""UpdateDB: Data import truncated at %s, Last DB entry: %s""", date, DB_datetime)
                    history = history [0:i]
                    break
                
                i += 1
                if i >= len (history):
                    log.warning("""UpdateDB: Did not reach end database date. Earliest imported record: %s, Last DB entry: %s""", date, DB_datetime)
                    break
            
            # filter data...
            if key == 'second':
                target = 0.0
                next = 0.0
                diff_1 = 0.001
                diff_2 = 0.010
                count_1 = 0
                count_2 = 0

                for i in range (0, len(history)):
                    # get current power value
                    power = history[i][2]

                    tmp = list(history[i])
                    filter = 0

                    # get the difference for previous point...
                    diff_previous = abs(power-target)
                    
                    # Get the difference for next point...
                    if i < len(history)-1:
                        next = history[i+1][2]
                        diff_next = abs(target-next)
                    else:
                        diff_next = 10000
                    
                    if diff_previous > diff_2 or diff_next > diff_2:
                        # dont filter, FILTER = 0
                        target = power
                    elif diff_previous < diff_1 and diff_next < diff_1:
                        # full filter, FILTER = 2
                        filter=2
                        count_2 += 1
                    else:
                        # medium filter, FILTER = 1
                        filter=1
                        count_1 += 1
                        
                    tmp.append(filter)
                    history[i] = tuple(tmp)
                    
                        
##                    print history[i][2], history[i][5]
##                print count_1, count_2, len(history), len(history)-count_1-count_2
            # insert history data
            db_history.InsertData (history)

        elif TED_datetime <= DB_datetime:
            log.info("""UpdateDB: DB datetime is equal or greater than TED current datetime. TED: %s, Last DB entry: %s. DB not updated since it us up to date.""",
                            TED_datetime, DB_datetime)

if __name__=="__main__":
    UpdateTEDDB()
