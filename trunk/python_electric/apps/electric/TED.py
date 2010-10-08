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

import urllib
import settings
import xml.etree.cElementTree as ET
from datetime import datetime, timedelta
import sys

import logging, logging.config

if __name__ <> 'python_electric.apps.electric.TED':
	logging.config.fileConfig(settings.LOG.CONFIGFILE)

log = logging.getLogger("python_electric.TED")

class APIBase:
    
    def __init__(self):

        """ 
            
        """
      
        self.GATEWAY_URL = settings.TED.GATEWAY_URL

        self.LIVE_DATA_URL = self.GATEWAY_URL + "/api/LiveData.xml"
        self.SYSTEM_SETTINGS_URL = self.GATEWAY_URL + "/api/SystemSettings.xml"
        self.UTILITY_SETTINGS_URL = self.GATEWAY_URL + "/api/UtilitySettings.xml"
        self.LOAD_PROFILE_CONFIG_URL = self.GATEWAY_URL + "/api/LoadProfileConfig.xml"
        self.HISTORY_URL = {'second' : self.GATEWAY_URL+"/history/secondhistory.xml?INDEX=0&MTU=%s&COUNT=%s",
                            'minute' : self.GATEWAY_URL+"/history/minutehistory.xml?INDEX=0&MTU=%s&COUNT=%s",
                            'hour'   : self.GATEWAY_URL+"/history/hourlyhistory.xml?INDEX=0&MTU=%s&COUNT=%s",
                            'day'    : self.GATEWAY_URL+"/history/dailyhistory.xml?INDEX=0&MTU=%s&COUNT=%s",
                            'month'  : self.GATEWAY_URL+"/history/monthlyhistory.xml?INDEX=0&MTU=%s&COUNT=%s"
                            }
        
        self.MAX_DATAPOINTS = { 'second' : 60*60,
                                'minute' : 48*60,
                                'hour'   : 7*24,
                                'day'    : 90,
                                'month'  : 10*12,
                                }

        self.XML_DATA = None

    def GetLiveData(self):
        self.GetURL(self.LIVE_DATA_URL)  
        
    def GetLoadProfileConfig(self):
        self.GetURL(self.LOAD_PROFILE_CONFIG_URL)
        
    def GetUtilitySettings(self):
        return self.GetURL(self.UTILITY_SETTINGS_URL)        
    
    def GetSystemSettings(self):
        return self.GetURL(self.SYSTEM_SETTINGS_URL)
  
    def GetURL(self, url, MTU=-1, count=-1):
        """ Returns a file-like object for the TED 5000 for the specified URL, MTU, and count
            
            GetURL (url, [MTU, [count]])
            
            if MTU and count are not included it will not be included in URL.
        """
        log.info("GetURL: Getting specified URL (%s)", url)
          
        if MTU > 0:
            url = url % (MTU, count + settings.TED.GATEWAY_COUNT_ADJUSTMENT)
       
        try:
            f = urllib.urlopen(url)
            tree = ET.parse(f)
            self.XML_DATA = tree.getroot()
            return 0
        except IOError:
            log.critical('GetURL: Unable to connect to TED @ %s.  Please check network connection and TED.GATEWAY_URL address in settings.py. (%s)', url, IOError.message)
            # should send an email
            return -1
        
    def GetRawXML(self, url, MTU=-1, count=-1):
        """ Returns a file-like object for the TED 5000 for the specified URL, MTU, and count
            
            GetURL (url, [MTU, [count]])
            
            if MTU and count are not included it will not be included in URL.
        """
        log.info("GetURL: Getting specified URL (%s)", url)
          
        if MTU > 0:
            url = url % (MTU, count + settings.TED.GATEWAY_COUNT_ADJUSTMENT)
       
        try:
            f = urllib.urlopen(url)
            return f.read()
        except IOError:
            log.critical('GetURL: Unable to connect to TED @ %s.  Please check network connection and TED.GATEWAY_URL address in settings.py. (%s)', url, IOError.message)
            # should send an email
            return -1
        
    def ParseXML(self, *pargs):
        elem = self.XML_DATA
        for key in pargs:
            try:
                elem = elem.findall(key)[0]
            except:
                return None
                
        if len(list(elem)) > 0:
            node = {}
            for n in elem:
                node[n.tag] = n.text
            return node
        else:
            return elem.text
        
    def DumpXML (self):
        return ET.dump(self.XML_DATA)
        #return ET.tostring(self.XML_DATA)
        
    def GetLastHistoryDate (self, key, MTU):
        history = self.GetHistory(key, MTU, 1)
        log.debug ("GetLastHistoryDate: history = %s", history)
        if history == []:
            log.warning("GetLastHistoryDate: No history found.  Returned %s. Maybe it hasn't collected enough data?", history)
            return None
        date = history[0][1]
        if date == []:
            log.warning("GetLastHistoryDate: No date found.  Returned %s. Maybe it hasn't collected enough data?", date)
            return None
        else:
            log.info("GetLastHistoryDate: %s", date)
            return date


class Gateway(APIBase):
    # Python Class that interfaces with TED5000 Gateway through the published API (xml format)
    
    ## API Elements...
    ## Live Data -------------------------------------------------------
  
    # Element Gateway Time
    def GatewayTime(self):
        """ The current system time of the gateway
            
            GetCurrentTime () - Returns datetime object
        """
        
        value = self.ParseXML("GatewayTime")
        
        log.debug("GatewayTime: %s", value)
    
        return datetime(int(value.get('Year'))+2000, int(value.get('Month')), int(value.get('Day')), int(value.get('Hour')), int(value.get('Minute')), int(value.get('Second')))
    
    # Element Voltage
    def Voltage(self, MTU=0, field='VoltageNow'):
        """ The voltage readings for the net (Total) and
            individual MTU's (MTU1 to MTU 4)
            
            Voltage(MTU, field) - returns specified field value
            
            MTU = 0 for Total (or leave unspecified)
            field = VoltageNow - The most recent voltage reading from the MTU
                    LowVoltageHour - The lowest voltage reading of the past hour
                    LowVoltageToday - The lowest voltage reading recorded today
                    LowVoltageTodayTimeHour - The hour (00-23) of the lowest 
                                            voltage reading recorded today
                    LowVoltageTodayTimeMin - The minute (00-59) of the lowest 
                                            voltage reading recorded today
                    HighVoltageHour - The most recent voltage reading from the MTU
                    HighVoltageToday - The Highest voltage reading of the past hour
                    HighVoltageTodayTimeHour - The hour (00-23) of the highest 
                                            voltage reading recorded today
                    HighVoltageTodayTimeMin - The minute (00-59) of the highest
                                            voltage reading recorded today
                    LowVoltageMTD - The lowest voltage recorded in the current 
                            billing period
                    LowVoltageMTDDateMonth - The month in which the low voltage
                            was recorded
                    LowVoltageMTDDateDay - The day of the month the low voltage
                            was recorded
                    HighVoltageMTD - The highest voltage recorded in the
                            current billing period
                    HighVoltageMTDDateMonth - The month in which the highest 
                            voltage was recorded
                    HighVoltageMTDDateDay - The day of the month the highest 
                            voltage was recorded
        """
        
        voltagefields = ('VoltageNow',
                        'LowVoltageHour',
                        'LowVoltageToday',
                        'HighVoltageHour',
                        'HighVoltageToday',
                        'LowVoltageMTD',
                        'HighVoltageMTD')
        datefields = (  'LowVoltageTodayTimeHour',
                        'LowVoltageTodayTimeMin',
                        'HighVoltageTodayTimeHour',
                        'HighVoltageTodayTimeMin',
                        'LowVoltageMTDDateMonth',
                        'LowVoltageMTDDateDay',                        
                        'HighVoltageMTDDateMonth',
                        'HighVoltageMTDDateDay')
                                                        
        assert field in (voltagefields or datefields),'unknown field %s'%field
                        
        if MTU >= 1 and MTU <= 4:
            value = self.ParseXML("Voltage", 'MTU' + str(MTU), field)
        else:
            value = self.ParseXML("Voltage", "Total", field)
    
        if value:
            if field in voltagefields:
                value = float(value)/10
            else:
                value = float(value)
            return value
        else:
            return None
    
    # Element Power and sub functions PowerNow, PowerTDY
    def Power(self, MTU=0, field=None):
        """ The Power readings for the net (Total) and
            individual MTU's (MTU1 to MTU 4)
            
            Power(MTU, field) - returns specified field value
            
            MTU = 0 for Total (or leave unspecified)
            
            Field
            PowerNow- The most recent Power reading from the MTU (Watts)
            PowerTDY- Cumulative Power since midnight (Watts)
            PowerMTD- Cumulative Power since the beginning of the
                billing cycle (Watts)
            PowerProj- Projected power usage this billing cycle (Watts)
            KVA- Most recent Kilovolt-ampere reading (VA)
            PowerAvg- The average daily power used this billing cycle (Watts)
            PeakTdy- The highest power reading read since midnight  Watts
            PeakMTD- Highest power reading this billing cycle       Watts

            PeakTdyHour- The hour when the peak reading occurred        00-23
            PeakTdyMin- The minute when the peak reading occurred      00-59
            PeakMTDMonth- The month in which the peak reading occurred    1-12
            PeakMTDDay-   The day of the month in which the peak reading  1-31
                            occurred
            MinTdy- The highest power reading read since midnight
            MinMTD- Highest power reading this billing cycle
            MinTdyHour- The hour when the Min reading occurred
            MinTdyMin- The minute when the Min reading occurred
            MinMTDMonth- The month in which the Min reading occurred
            MinMTDDay- The day of the month in which the Min reading
                         occurred

        """

        powerfields = ( 'PowerNow',
                        ##'PowerHour',  ??
                        'PowerTDY',
                        'PowerMTD',
                        'PowerProj',
                        'KVA',
                        'PeakTdy',
                        'PeakMTD',
                        'MinTdy',
                        'MinMTD')

        datefields = (  'PeakTdyHour',
                        'PeakTdyMin',
                        'PeakMTDMonth',
                        'PeakMTDDay',
                        'MinTdyHour',
                        'MinTdyMin',
                        'MinMTDMonth',
                        'MinMTDDay',
                        'PowerAvg')

        assert field in (powerfields or datefields),'unknown field %s'%field
        assert MTU in [0,1,2,3,4],'unknown MTU #%s'%MTU
                        
        if MTU >= 1 and MTU <= 4:
            value = self.ParseXML("Power", 'MTU' + str(MTU), field)
        else:
            value = self.ParseXML("Power", "Total", field)
    
        if value:
            if field in powerfields:
                value = float(value)/1000
            else:
                ## Check this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                value = int(value)
            return value
        else:
            return None

    def Cost(self, MTU=0, field=None):
        """ The Cost readings for the net (Total) and
            individual MTU's (MTU1 to MTU 4)
    
        """
        pass
   
        
    def Utility(self, field=''):
        """ Utility specific information used by the
            Dashboard

    
        """
        pass
        
    ## Historical Data --------------------------------------------------
    def GetHistory(self, key, MTU, count):
        
        assert key in ('second','minute','hour','day','month'),\
            'unknown time frame key %s'%key
        
        max = self.MAX_DATAPOINTS.get(key)
        if count >= max:
            log.info("GetHistory: Maximum number of datatpoints reached (%s >= %s MAX)", count, max)
            count = max
        url = self.HISTORY_URL.get(key)
        
       
        # Get a file-like object for the TED 5000
        log.info("GetHistory: Retrieving history from TED5000 MTU=%s..." % (MTU))
           
        url = url % (MTU, count + settings.TED.GATEWAY_COUNT_ADJUSTMENT)
       
        try:
            f = urllib.urlopen(url)
        except IOError:
            log.critical('GetHistory: Unable to connect to TED @ %s.  Please check network connection and TED.GATEWAY_URL address in settings.py. (%s)', url, IOError.message)
            # should send an email
            sys.exit('GetHistory: Unable to connect to TED @ %s.  Please check network connection and TED.GATEWAY_URL address in settings.py. (%s)'% (url, IOError.message))

        log.info("GetHistory: Done.  Parsing data...")

        tree = ET.parse(f)
        level_1 = tree.getroot()

        mtus = []
        date = []
        power = []
        cost = []
        voltage = []

        for level_2 in list(level_1):
            for level_3 in list(level_2):
                if level_3.tag == "MTU":        # used in all history
                    mtus.append(int(level_3.text))
                elif level_3.tag == "DATE":     # used in all history
                    date.append(datetime.strptime(level_3.text, "%m/%d/%Y %H:%M:%S"))
                elif level_3.tag == "POWER":    # used in all history
                    power.append(float (level_3.text)/1000)
                elif level_3.tag == "COST":     # used in all history
                    cost.append(float (level_3.text)/100)
                elif level_3.tag == "VOLTAGE":  # second, minute only
                    voltage.append(float (level_3.text)/10)
        f.close()
        
        if len(voltage) > 0:
            matrix = map(None, mtus, date, power, cost, voltage) # second and minute
        else:
            matrix = map(None, mtus, date, power, cost) # hour history
            #, vmin, vmax, pmin, pmax, cmin, cmax)

        log.debug ("GetHistory: first 5 history items: %s", matrix[0:4])

        d_last = datetime(2000, 1, 1)
        u = 0
        while u < len(matrix):
            d_current = matrix[u][1]
            if d_current == d_last:
                log.warning("GetHistory: Duplicate dates (%s = %s @ row %s). URL:%s.", d_last, d_current, u, url)
                del matrix[u]
                continue
            d_last = d_current
            u += 1

        log.info("DONE.")

        len_matrix = len(matrix)
        if len_matrix > 0:
            log.info("GetHistory: MTU:%s - %s records requested, %s records returned", MTU, count, len_matrix)
        else:
            log.error("GetHistory: ERROR! MTU:%s  (%s) records requested (%s returned). Not enough data? URL: %s.", MTU, count, len_matrix, url)
            print("GetHistory: ERROR! MTU:%s  (%s) records requested (%s returned). Not enough data? URL: %s." % (MTU, count, len_matrix, url))

        return matrix

    ## Load Profile Config ----------------------------------------------
    def NumberOfDevices(self):
        """ The number of devices that have been configured
            on the gateway
            
            returns Number

        """
        pass

    def HighestKey(self):
        """ Highest Key Each new device uses a unique key to help
            identify it within the gateway

            returns Number
        """
        pass
        
    def LoadProfileDevice(self):
        """ Element and Sub-elements that contain information about a specific
            load profile device

        """
        pass
    
    
    ## Settings
    # Utility Settings
    def Seasons(self):
        """ The Season configuration for the utility
        """
        pass
        
    def TOU(self):
        """ TOU Configuration info if the TOU tiered type
            is selected
        """
        pass
        
    def Tier(self):
        """ The Tier configuration if a "Tiered" rate type is
            selected by the user

        """
        pass
    
    def Demand(self):
        """ Future Use
        """
        return None
    
    def EnergyRates(self):
        """ EnergyRate set up per Season, Step, and TOU
            level.

        """
        pass
        
    def AdditionalCharges(self):
        """ Additional Charges that are applied to the
            utility rate (Per Season)

        """
        pass

    # System Settings
    def NumberMTU(self):
        """
        Returns the number of MTU's configured in the system
        
        NumberMTU() - returns integer
        """
        value = self.ParseXML("NumberMTU")

        if value:
            return int(value)
        else:
            return None
        
    def DemoMode(self):
        """ NOT USED
        
        """
        return None
    
    def NumberDisplay(self):
        """ The number of displays currently configured in
            the system

        """
        pass
        
    def DateTime(self):
        """ Date and Time configuration for the TED 5000

        """
        pass
        
    def Solar(self):
        """ "Advanced" MTU settings
        """
        pass
        
    def MTUs(self):
        """ Setup information for each MTU
        """
        pass
        
    def Gateway(self):
        """ Gateway Information
        """
        pass
        
    def Displays(self):
        """ Configuration information for the display
        """
        pass
        
    def UserInterface(self):
        """ Settings for the Footprints User Interface
        """
        pass
        
    def NetworkSettings(self):
        """ Network Settings for the TED 5000
        """
        value = self.ParseXML("NetworkSettings")
        
        return value
    
    def GatewayTransmitGain(self):
        """ The PLC TX gain used by the gateway
        """
        value = self.ParseXML("GatewayTransmitGain")
        
        if int(value) == 0:
            return 3.0
        elif int(value) == 1:
            return 2.0
        else:
            return None
    
    def GatewayTransmitAmplifier(self):
        """ The amplifier level of the PLC modem on the MTU/Gateway


        """
        value = self.ParseXML("GatewayTransmitAmplifier")
        
        if int(value) == 2:
            return 1.0
        elif int(value) == 1:
            return 0.75
        elif int(value) == 0:
            return 0.5
        else:
            return None
    
    def GatewayNoiseBlanker(self):
        """ Whether or Not the noise blanker is enabled on
            the MTU/Gateway
            
            returns True (ON), False (OFF), None (ie. not found)
        """
        value = self.ParseXML("GatewayNoiseBlanker")
        
        if int(value) == 1:
            return True
        elif int(value) == 2:
            return False
        else:
            return None
    
    def Username(self):
        """ The username of the password protected user
            on the device
        """
        value = self.ParseXML("Username")
        
        return value
    
    def PasswordAll(self):
        """ Whether or not all screens on Footprints should
            be password protected
            
            returns True, False, None (ie. not found)
        """
        value = self.ParseXML("PasswordAll")
        
        if int(value) == 1:
            return True
        elif int(value) == 0:
            return False
        else:
            return None
    
    def PasswordConf(self):
        """ Whether or not the system configuration
            settings should be password protected
            
            returns True, False, None (ie. not found)
        """
        value = self.ParseXML("PasswordConf")
        
        if int(value) == 1:
            return True
        elif int(value) == 0:
            return False
        else:
            return None
    
    def GooglePowerMeter(self):
        """ Whether or not the device has been activated
            for Google PowerMeter
            
            returns True, False, None (ie. not found)
        """
        value = self.ParseXML("GooglePowerMeter")
        
        if int(value) == 1:
            return True
        elif int(value) == 0:
            return False
        else:
            return None
    
    def SendStatusGoogle(self):
        """ Whether or not statistical runtime information is 
            being sent to Google
            
            returns True, False, None (ie. not found)
        """
        value = self.ParseXML("SendStatusGoogle")
        
        if int(value) == 1:
            return True
        elif int(value) == 0:
            return False
        else:
            return None
        
    # Extra function not in the API
    def PowerNow(self, MTU=0):
        """ 
        Returns the most recent Power reading for the specified MTU in kW.  If no MTU is selected, returns total.
                    
        PowerNow () - returns float
        """
        if MTU >= 1 and MTU <= 4:
            value = self.ParseXML("Power", 'MTU' + str(MTU), "PowerNow")
        else:
            value = self.ParseXML("Power", "Total", "PowerNow")
    
        if value:
            value = float(value)/1000
            return value
        else:
            return None
        
    
    def PowerTDY(self, MTU=0):
        """ 
        Returns the cummulative Power for the day from the TED gateway
            
        PowerTDY () - returns float
        """
        if MTU >= 1 and MTU <= 4:
            value = self.ParseXML("Power", 'MTU' + str(MTU), "PowerTDY")
        else:
            value = self.ParseXML("Power", "Total", "PowerTDY")
   
        if value:
            return float(value)/1000
        else:
            return 100    

        


if __name__=="__main__":
    
    # Initialize object...
    TED = Gateway ()
    
    # Set logger...
##    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
##    ch = logging.StreamHandler()
##    ch.setLevel(logging.WARNING)
##    ch.setFormatter(formatter)
##    TED.logger.setLevel(logging.WARNING)
##    TED.logger.addHandler(ch)
    
    # get live data...
    TED.GetLiveData ()  
    
    # Check gateway time...
    GatewayTime = TED.GatewayTime()
    print "\nGatewayTime: %s\n" % GatewayTime
##    print TED.DumpXML()
    
    print "\nLive Data..."
    for i in range(0,5):
        print "\tVoltage (MTU: %s) %sV" % (i, TED.Voltage(i,'VoltageNow'))
        print "\tPower KVA (MTU: %s) %sVA" % (i, TED.Power(i,'KVA'))
        print "\tPowerNow (MTU: %s) %skW" % (i, TED.PowerNow(i))
        print "\tPowerTDY (MTU: %s): %skW" % (i, TED.PowerTDY(i))
    
    TED.GetSystemSettings()
    print "\nNumberMTU = %s" % TED.NumberMTU()

    print "\nThis should None since GetLiveData was closed: TED.PowerNow() = %s\n" % TED.PowerNow(0)

    print "Get last 5 history items (MTU=0)..."
    for k in ['second', 'minute', 'hour', 'day', 'month']:
        print '\t', TED.GetHistory(k, 0, 5)
    
    print "\nGetting last date for each history item (MTU=0)..."
    for k in ['second', 'minute', 'hour', 'day', 'month']:
        print '\t', TED.GetLastHistoryDate (k, 0)
        
    TED.GetSystemSettings()
    
    print "\nNetwork Settings... "
    table = TED.NetworkSettings()
    for k in table.keys():
        print '\t', k, '\t', table[k]
        
    print 
    print "Gateway Transmit Gain: ", TED.GatewayTransmitGain()
    print "Gateway Transmit Amplifier: ", TED.GatewayTransmitAmplifier()
    print "Google PowerMeter: ", TED.GooglePowerMeter()
    print "Send status to Google: ", TED.SendStatusGoogle()
    
##    print TED.GetRawXML(TED.LIVE_DATA_URL)
