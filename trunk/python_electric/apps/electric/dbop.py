import MySQLdb
import sys
import logging, logging.config
import settings

logging.config.fileConfig(settings.LOG.CONFIGFILE)
log = logging.getLogger("python_electric.dbop")

class GenericDBOP:
    # Generic DB object, contains basic function for all tables

    def __init__(self, db, name):
        self.db = db                #database connection
        self.name = name            #table name
        self.dbc = self.db.cursor() #cursor object
        
    def deleteall():
        pass
        # executes "DELETE FROM `django_electric`.`TED_history_second`"
##        q = "DELETE FROM %s" % (self.name)
##        self.dbc.execute(q)

    def PurgeOldData():
        # checks to see if a setting.dayspurge value > 0, and cleans
        # database for entries older than x days
        pass
        
    def CreateTable(self):
        # check to see if the table exists, if not create one.
        pass
        
    def GetMinDate(self, MTU):
        q = "select MIN(date) from %s where MTU = %s" % (self.name, MTU)
        
        log.info("GetMinDate: q = %s", q)
        
        try:
            # executes a query (but doesn't return the data)
            self.dbc.execute(q)
        except MySQLdb.Error, e:
            # if there is an error executing, log error and exit
            log.critical ("Error %s: %s", e.args[0], e.args[1])
            sys.exit ("Error %d: %s" % (e.args[0], e.args[1]))
        
        # fetches the data from the most recently executed query.
        result = self.dbc.fetchone()    
        
        if len(result) > 0:
            log.info("GetMinDate: %s", result[0])
            return result[0]
        else:
            log.error("GetMinDate: error")
            return 0
        
    def GetMaxDate(self, MTU):
        q = "select MAX(date) from %s where MTU = %s" % (self.name, MTU)
        
        log.info("GetMaxDate: q = %s", q)
        
        try:
            self.dbc.execute(q)         # executes a query (but doesn't return the data)
        except MySQLdb.Error, e:        # if there is an error executing, log error and exit
            log.critical ("Error %s: %s", e.args[0], e.args[1])
            sys.exit ("Error %d: %s" % (e.args[0], e.args[1]))
        
        result = self.dbc.fetchone()    # fetches the data from the most recently executed query.
        
        if len(result) > 0:
            log.info("GetMaxDate: %s", result[0])
            return result[0]
        else:
            log.error("GetMaxDate: error")
            return 0
        
    def GetHistory(self, MTU, datestart=None, dateend=None):
        
        ## assert that datestart, dateend are dates
        ## use elif to make sure the bottom works, if not sys.exit
        if datestart == None and dateend == None:
            q = "select * from %s where MTU = %s order by DATE" % (self.name, MTU)
        if datestart <> None and dateend == None:
            q = "select * from %s where MTU = %s and DATE >= '%s' order by DATE" % (self.name, MTU, datestart)
        if datestart <> None and dateend <> None:
            q = "select * from %s where MTU = %s and DATE between '%s' and '%s' order by DATE" % (self.name, MTU, datestart, dateend)
        
        log.info("GetHistory: q = %s", q)
        
        try:
            self.dbc.execute(q)         # executes a query (but doesn't return the data)
        except MySQLdb.Error, e:        # if there is an error executing, log error and exit
            log.critical ("Get History: Error %s: %s (id 1)", e.args[0], e.args[1])
            sys.exit ("Get History: Error %d: %s (id 1)" % (e.args[0], e.args[1]))
        
        result = self.dbc.fetchall()    # fetches the data from the most recently executed query.
        
        if len(result) > 0:
            log.info("Get History: %s records fetched (id 2). ", len(result))
            return result
        else:
            log.error("Get History: Error (Result = %s, q = %s (id 3)", result, q)
            return None

class TED_DBOP (GenericDBOP):
    # DB object to store information from TED5000
    
    def InsertData(self, zipped):
        log.info("InsertData: insert %s records in table '%s'...", len(zipped), self.name)
        if len(zipped[0]) == 4:
            q = "INSERT INTO %s " % (self.name) + " (MTU, DATE, POWER, COST) VALUES (%s, %s, %s, %s)" 
        elif len(zipped[0]) == 5:
            q = "INSERT INTO %s " % (self.name) + " (MTU, DATE, POWER, COST, VOLTAGE) VALUES (%s, %s, %s, %s, %s)"
        elif len(zipped[0]) == 6:
            q = "INSERT INTO %s " % (self.name) + " (MTU, DATE, POWER, COST, VOLTAGE, FILTER) VALUES (%s, %s, %s, %s, %s, %s)"

        log.info("Preparing to insert data query = '%s'", q)            
        try:
            self.dbc.executemany(q, zipped)
        except MySQLdb.Error, e:        # if there is an error executing, log error and exit
            log.critical ("Error %s: %s", e.args[0], e.args[1])
        
        log.info("DONE.")
        
  
class RunningAveragesDBOP (GenericDBOP):

    def InsertData(self, zipped):
        log.info("InsertData: insert %s records in table '%s'...", len(zipped), self.name)
        q = "INSERT INTO %s " % (self.name) + " (MTU, DATE, POWER7, POWER14, POWER21, POWER28) VALUES (%s, %s, %s, %s, %s, %s)" 
        
        try:
            self.dbc.executemany(q, zipped)
        except MySQLdb.Error, e:        # if there is an error executing, log error and exit
            log.critical ("Error %s: %s", e.args[0], e.args[1])
        
        log.info("DONE.")
    
