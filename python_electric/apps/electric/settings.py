import os

ELECTRIC_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.sep.join(ELECTRIC_APP_PATH.split(os.sep)[0:-2])

ADMINS = (
    ('username', 'user@gmail.com'),
)

class ELECTRICITY():
    # default electricity rate:
    RATE = 0.08

class CHART():
    BUDGET_DAY = [2.464, 8.061, 7.433, 10.693]
    BUDGET_WEEK = [28.651, 28.651, 28.651, 28.651, 28.651, 28.651, 28.651]
    Y_MAX = 3 # sets the initial maximum view in usage charts (kW h)
    WIDTH = 700
    PATH = os.path.join(PROJECT_PATH, 'media', 'charts')

    # top opaque light green on historical data
    COLOR_HISTORICAL_1 = 'b4ecb4' 
    
    # bottom opaque dark green on historical data
    COLOR_HISTORICAL_2 = '5a9f59'
    
    # top bright light green on current data
    COLOR_CURRENT_1 = '70d070'
    # bottom bright dark green on current data
    COLOR_CURRENT_2 = '1d7f17' 

    # dark current 
    COLOR_CURRENT_3 = '155811'

    # running averages...
    COLOR_7 = 'D3D3D3'
    COLOR_14 = 'black'
    COLOR_21 = 'red'
    COLOR_28 = COLOR_CURRENT_3


class LOG():
    CONFIGFILE = os.path.join(ELECTRIC_APP_PATH, 'logging.conf')

class DATABASE():
    # Database connection information
    NAME = 'django_electric'
    USER = 'django_electric'
    PASSWORD = 'phe6EpHu' 

    TABLES = {'second': "TED_history_second",
              'minute': "TED_history_minute",
              'hour'  : "TED_history_hour",
              'day'   : "TED_history_day",
              'month' : "TED_history_month",
              }
    
class TED():
    # URL of TED 5000 gateway (ie http://TED5000
    GATEWAY_URL = "http://TED5000"

    # number of MTUs
    MTU = 1  ## for future implemenation

    # extra seconds imported each time for good measure
    IMPORT_OVERLAP = 30

    # number of second data points (60 min * 60 sec)
    MAX_DATA_POINTS = 60 * 60 

    GATEWAY_COUNT_ADJUSTMENT = 1

    DATABASE_TABLE = "TED_history_second" # will be eliminated
    
                #   DB Table Name,  Url,  Max Data Points,  
    DB_URL_MAP = (("TED_history_second", GATEWAY_URL+"/history/secondhistory.xml?INDEX=0&MTU=%s&COUNT=%s", 60*60, 1),
                  ("TED_history_minute", GATEWAY_URL+"/history/minutehistory.xml?INDEX=0&MTU=%s&COUNT=%s", 48*60, 60),
                  ("TED_history_hour", GATEWAY_URL+"/history/hourlyhistory.xml?INDEX=0&MTU=%s&COUNT=%s", 7*24, 60*60),
                  ("TED_history_day", GATEWAY_URL+"/history/dailyhistory.xml?INDEX=0&MTU=%s&COUNT=%s", 90, 60*60*24 ),
                  ("TED_history_month", GATEWAY_URL+"/history/monthlyhistory.xml?INDEX=0&MTU=%s&COUNT=%s", 10*12, 60*60*24*30),
                )

    DB_MAP = (('second', "TED_history_second", 1),
                  ('minute', "TED_history_minute", 60),
                  ('hour', "TED_history_hour", 60*60),
                  ('day', "TED_history_day", 60*60*24 ),
                  ('month', "TED_history_month", 60*60*24*30),
                )


