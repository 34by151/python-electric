from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from python_electric.apps.electric.models import TED_history_second, TED_history_minute, TED_history_hour, TED_history_day, TED_history_month

import datetime, string
from GChartWrapper import *
from charts import CreateWeeklyBudgetChart
from settings import CHART


width = CHART.WIDTH
width = 1000


def bar_weekbudget(request):
    title = "Budget Chart Tests (testviews.py)"
    
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    
    week_start = now - datetime.timedelta(days=int(now.strftime('%w')))
    week_start = datetime.datetime(week_start.year, week_start.month, week_start.day)

    test = [
            #[[24, 24, 24, 24, 24, 24, 24],[3, 0, 0, 0, 0, 0, 0], week_start + datetime.timedelta (hours=3)  ],
            #[[24, 24, 24, 24, 24, 24, 24],[24, 3, 0, 0, 0, 0, 0], week_start + datetime.timedelta (hours=3, days=1)],
            #[[24, 24, 24, 24, 24, 24, 24],[24, 24, 3, 0, 0, 0, 0], week_start + datetime.timedelta (hours=3, days=2)  ],
            #[[24, 24, 24, 24, 24, 24, 24],[24, 24, 24, 3, 0, 0, 0],week_start + datetime.timedelta (hours=3, days=3)  ],
            #[[24, 24, 24, 24, 24, 24, 24],[24, 24, 24, 24, 3, 0, 0],week_start + datetime.timedelta (hours=3, days=4)  ],
            #[[24, 24, 24, 24, 24, 24, 24],[24, 24, 24, 24, 24, 3, 0],week_start + datetime.timedelta (hours=3, days=5)  ],
            #[[24, 24, 24, 24, 24, 24, 24],[24, 24, 24, 24, 24, 24, 3,],week_start + datetime.timedelta (hours=3, days=6) ],
            #[[24, 24, 24, 24, 24, 24, 24],[24, 23.5, 0, 0, 0, 0, 0], week_start + datetime.timedelta (minutes=30, days=1)  ],
            #[[24, 24, 24, 24, 24, 24, 24],[24, 0.5, 0, 0, 0, 0, 0], week_start + datetime.timedelta (hours=23, minutes=30, days=1)  ],
            [[24, 24, 24, 24, 24, 24, 24],[12, 12, 12, 12, 12, 12, 12],datetime.datetime(2010, 6, 13, 0, 0, 0)  ],
            [[24, 24, 24, 24, 24, 24, 24],[36, 36, 36, 36, 36, 36, 36],datetime.datetime(2010, 6, 13, 0, 0, 0)  ],
            #[[24, 24, 24, 24, 24, 24, 24],[24, 24, 24, 24, 24, 24, 22],datetime.datetime(2010, 6, 13, 0, 0, 0)  ],
            #[[24, 24, 24, 24, 24, 24, 24],[24, 24, 24, 24, 24, 24, 22],datetime.datetime(2010, 6, 13, 0, 0, 0)  ],
            [[28.651, 28.651, 28.651, 28.651, 28.651, 28.651, 28.651],[22.651, 34.651, 28.651, 28.651, 28.651, 28.651, 34.651],datetime.datetime(2010, 6, 13, 0, 0, 0)  ],
            
            ]

    data = []

    for item in test:
        budget, current, date = item
        u = CreateWeeklyBudgetChart (date.year, int(date.strftime('%U')), current, budget)
        data.append(u)
        


    return render_to_response ('electric/bar_budget.html', {'data' : data}, context_instance=RequestContext(request))



def bar_budget(request):
    title = "Budget Chart Tests (testviews.py)"

    test = [
                [[6, 6, 6, 6], [0.5, 0, 0, 0], datetime.datetime(2010, 6, 10, 0, 30, 0)  ],
                [[6, 6, 6, 6], [0.6, 0, 0, 0], datetime.datetime(2010, 6, 10, 0, 30, 0)  ],
                [[6, 6, 6, 6], [0.7, 0, 0, 0], datetime.datetime(2010, 6, 10, 0, 30, 0)  ],
                [[6, 6, 6, 6], [0.8, 0, 0, 0], datetime.datetime(2010, 6, 10, 0, 30, 0)  ],
                [[6, 6, 6, 6], [0.9, 0, 0, 0], datetime.datetime(2010, 6, 10, 0, 30, 0)  ],
                [[6, 6, 6, 6], [1, 0, 0, 0], datetime.datetime(2010, 6, 10, 1, 0, 0)  ],
                [[6, 6, 6, 6], [2, 0, 0, 0], datetime.datetime(2010, 6, 10, 2, 0, 0)  ],
                [[6, 6, 6, 6], [3, 0, 0, 0], datetime.datetime(2010, 6, 10, 3, 0, 0)  ],
                [[6, 6, 6, 6], [4, 0, 0, 0], datetime.datetime(2010, 6, 10, 4, 0, 0)  ],
                [[6, 6, 6, 6], [5, 0, 0, 0], datetime.datetime(2010, 6, 10, 5, 0, 0)  ],
                [[6, 6, 6, 6], [6, 0, 0, 0], datetime.datetime(2010, 6, 10, 6, 0, 0)  ],
                
                [[6, 6, 6, 6], [6, 0.5, 0, 0], datetime.datetime(2010, 6, 10, 6, 30, 0)  ],
                [[6, 6, 6, 6], [6, 0.6, 0, 0], datetime.datetime(2010, 6, 10, 6, 30, 0)  ],
                [[6, 6, 6, 6], [6, 0.7, 0, 0], datetime.datetime(2010, 6, 10, 6, 30, 0)  ],
                [[6, 6, 6, 6], [6, 0.8, 0, 0], datetime.datetime(2010, 6, 10, 6, 30, 0)  ],
                [[6, 6, 6, 6], [6, 0.9, 0, 0], datetime.datetime(2010, 6, 10, 6, 30, 0)  ],
                [[6, 6, 6, 6], [6, 1, 0, 0], datetime.datetime(2010, 6, 10, 7, 0, 0)  ],
                [[6, 6, 6, 6], [6, 2, 0, 0], datetime.datetime(2010, 6, 10, 8, 0, 0)  ],
                [[6, 6, 6, 6], [6, 3, 0, 0], datetime.datetime(2010, 6, 10, 9, 0, 0)  ],
                [[6, 6, 6, 6], [6, 4, 0, 0], datetime.datetime(2010, 6, 10, 10, 0, 0)  ],
                [[6, 6, 6, 6], [6, 5, 0, 0], datetime.datetime(2010, 6, 10, 11, 0, 0)  ],
                [[6, 6, 6, 6], [6, 6, 0, 0], datetime.datetime(2010, 6, 10, 12, 0, 0)  ],
                                
                [[6, 6, 6, 6],    [6, 6, 0.5, 0], datetime.datetime(2010, 6, 10, 12, 30, 0) ],
                [[6, 6, 6, 6],    [6, 6, 0.6, 0], datetime.datetime(2010, 6, 10, 12, 30, 0) ],
                [[6, 6, 6, 6],    [6, 6, 0.7, 0], datetime.datetime(2010, 6, 10, 12, 30, 0) ],
                [[6, 6, 6, 6],    [6, 6, 0.8, 0], datetime.datetime(2010, 6, 10, 12, 30, 0) ],
                [[6, 6, 6, 6],    [6, 6, 0.9, 0], datetime.datetime(2010, 6, 10, 12, 30, 0) ],
                [[6, 6, 6, 6],    [6, 6, 1, 0], datetime.datetime(2010, 6, 10, 13, 0, 0) ],
                [[6, 6, 6, 6],    [6, 6, 2, 0], datetime.datetime(2010, 6, 10, 14, 0, 0) ],
                [[6, 6, 6, 6],    [6, 6, 3, 0], datetime.datetime(2010, 6, 10, 15, 0, 0) ],
                [[6, 6, 6, 6],    [6, 6, 4, 0], datetime.datetime(2010, 6, 10, 16, 0, 0) ],
                [[6, 6, 6, 6],    [6, 6, 5, 0], datetime.datetime(2010, 6, 10, 17, 0, 0) ],
                [[6, 6, 6, 6],    [6, 6, 6, 0], datetime.datetime(2010, 6, 10, 18, 0, 0) ],
                
                [[6, 6, 6, 6],    [6, 6, 6, 0.5], datetime.datetime(2010, 6, 10, 18, 30, 0) ],
                [[6, 6, 6, 6],    [6, 6, 6, 0.6], datetime.datetime(2010, 6, 10, 18, 30, 0) ],
                [[6, 6, 6, 6],    [6, 6, 6, 0.7], datetime.datetime(2010, 6, 10, 18, 30, 0) ],
                [[6, 6, 6, 6],    [6, 6, 6, 0.8], datetime.datetime(2010, 6, 10, 18, 30, 0) ],
                [[6, 6, 6, 6],    [6, 6, 6, 0.9], datetime.datetime(2010, 6, 10, 18, 30, 0) ],
                [[6, 6, 6, 6],    [6, 6, 6, 1], datetime.datetime(2010, 6, 10, 19, 0, 0) ],
                [[6, 6, 6, 6],    [6, 6, 6, 2], datetime.datetime(2010, 6, 10, 20, 0, 0) ],
                [[6, 6, 6, 6],    [6, 6, 6, 3], datetime.datetime(2010, 6, 10, 21, 0, 0) ],
                [[6, 6, 6, 6],    [6, 6, 6, 4], datetime.datetime(2010, 6, 10, 22, 0, 0) ],
                [[6, 6, 6, 6],    [6, 6, 6, 5], datetime.datetime(2010, 6, 10, 23, 0, 0) ],
                [[6, 6, 6, 6],    [6, 6, 6, 6], datetime.datetime(2010, 6, 10, 23, 59, 0) ],
                
                [[6, 6, 6, 6],    [12, 12, 12, 12], datetime.datetime(2010, 6, 10, 23, 59, 0) ],
                [[6, 6, 6, 6],    [3, 3, 3, 3], datetime.datetime(2010, 6, 10, 23, 59, 0) ],
                
                [[2, 8, 7, 10], [2, 8, 17, 4], datetime.datetime(2010, 6, 10, 23, 59, 0)],
                [[2, 8, 7, 9.9999999999], [2, 8, 17, 4], datetime.datetime(2010, 6, 10, 23, 59, 0)],
                [[2.464, 8.0609999999999999, 7.4329999999999998, 10.693], [2.7370000000000001, 5.9089999999999998, 2.023, 0], datetime.datetime (2010, 7, 18, 12, 33)],
                [[2.464, 8.0609999999999999, 7.4329999999999998, 10.693], [2.7370000000000001, 5.9089999999999998, 15.023, 8.8369999999999997], datetime.datetime (2010, 7, 18, 20, 33)],
            ]
                
    data = []

    for item in test:
        budget, current, date = item
        u = CreateDayBudgetChart (date, current, budget)
        data.append(u)
        
    return render_to_response ('electric/bar_budget.html', {'data' : data}, context_instance=RequestContext(request))
    
def CreateDayBudgetChart (date, current, budget):
    
    #now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    now = date
    
  
    if date.year == now.year and date.month == now.month and date.day == now.day:
        time = datetime.time (now.hour, now.minute)
    else:
        time = datetime.time (23, 59)

    current_sum = 0.0
    for i in current:
        current_sum += i
    
    historical_total = 0.0
    for i in budget:
        historical_total += i
        
    kw_max = max(current_sum, historical_total)
    
    historical_sum = 0.0
    if time < datetime.time (6,0):
        historical_sum = budget[0] * (time.hour + time.minute/60.0) / 6 
    elif time < datetime.time (12,0):
        historical_sum = budget[0] + budget[1] * (time.hour + time.minute/60.0 - 6) / 6 
    elif time < datetime.time (18,0):
        historical_sum = budget[0] + budget[1] + budget[2] * (time.hour + time.minute/60.0 - 12) / 6 
    else:
        historical_sum = budget[0] + budget[1] + budget[2] + budget[3] * (time.hour + time.minute/60.0 - 18) / 6 
        
    if historical_sum > 0:
        percentage = (current_sum - historical_sum) / historical_sum
    else:
        percentage = 0.0
        
    
    if percentage > 0.01 :
        # worse than expected... red
        color = 'e0b070'
        color_marker = 'a06000'
    elif percentage < -0.01:
        # better than expected... green
        color = '70d070'
        color_marker = '008000'
    else:
        # about even... yellow
        color = 'd8d870'
        color_marker = '909000'
        
    c_max =  1.0/kw_max
    #pixel_max = 900
    pixel_max = width - 1000
    c_label = current_sum/historical_total
    if c_label > 1:
        c_label = 1.0
    
    c_sq501 = current[0]*c_max
    c_night = c_sq501/2
    c_sq502 = (current[0]+current[1])*c_max
    c_morning = (c_sq502-c_sq501)/2 + c_sq501
    c_sq503 = (current[0]+current[1]+current[2])*c_max
    c_afternoon = (c_sq503-c_sq502)/2  + c_sq502
    c_evening = (c_label-c_sq503)/2  + c_sq503
    
    b_max =  historical_total/kw_max
    #pixel_max = 883
    pixel_max = width - 115
    b_label = b_max
    
    b_length = pixel_max*b_max
    
    b_sq501 = budget[0]/historical_total*b_max
    
    b_night = b_sq501/2
    b_sq502 = (budget[0]+budget[1])/historical_total*b_max
    b_morning = (b_sq502-b_sq501)/2 + b_sq501
    b_sq503 = (budget[0]+budget[1]+budget[2])/historical_total*b_max
    b_afternoon = (b_sq503-b_sq502)/2  + b_sq502
    b_evening = (b_max-b_sq503)/2  + b_sq503

    G = HorizontalBarStack([ [current_sum/kw_max * 100],[0,historical_sum/kw_max * 100] ], encoding='text') 
    G.color(color, '666666')
    
    G.size(width,34)
    G.margin(20,0,0,0)
    G.bar(13,1,1)
    G.axes('xyr')
    G.axes.label(2, str(round(historical_total,1)) + ' kWh expected', str(round(current_sum,1)) + ' kWh used')
    G.axes.style(0,'ffffff',0,0,'t')
    G.axes.style(1,'ffffff',10,1,'t')
    G.axes.style(2,'ffffff',10,-1,'t','ffffff')
    G.axes.tick(0,0)
    G.axes.tick(1,0)
    G.axes.tick(2,6)

# CURRENT
    if c_sq501 > 0.04:
        c_sq501_label = 'night'
    elif c_sq501 > 0.03:
        c_sq501_label = 'ngt.'
    else:
        c_sq501_label = ''
        
    if c_sq502-c_sq501 > 0.05:
        c_sq502_label = 'morning'
    elif c_sq502-c_sq501 > 0.03:
        c_sq502_label = 'mor.'
    else:
        c_sq502_label = ''

    if c_sq503-c_sq502 > 0.06:
        c_sq503_label = 'afternoon'
    elif c_sq503-c_sq502 > 0.04:
        c_sq503_label = 'aftn.'
    else:
        c_sq503_label = ''

    if c_label-c_sq503 > 0.05:
        c_sq504_label = 'evening'
    elif c_label-c_sq503 > 0.03:
        c_sq504_label = 'eve.'
    else:
        c_sq504_label = ''
        

    #G.marker (r"@ysq'i\=999'=13'scl'\fff'c", '', 0, '0.5:1', 0, -1) # no light grey area!!!
    G.marker ("@y%s\'h\\=10\'f\\fff\'c\\h-0-10\'a\\<=66\'\'scl\'" % c_sq501_label, '', 0, '0:' + str(c_night), 0) # adds 'night' to current
        
    if time > datetime.time (6,0):
        G.marker ("@ysq75\'i\\=1\'=13\'scl\'\\fff\'c", '', 0, '0:' + str(c_sq501), 0) # adds night divider current
        G.marker ("@y%s\'h\\=10\'f\\fff\'c\\h-0-10\'a\\<=184\'\'scl\'" % c_sq502_label, '', 0, '0:' + str(c_morning), 0) # adds 'morning' to current
        
    if time > datetime.time (12,0):
        G.marker ("@ysq75\'i\\=1\'=13\'scl\'\\fff\'c", '', 0, '0:' + str(c_sq502), 0)
        G.marker ("@y%s\'h\\=10\'f\\fff\'c\\h-0-10\'a\\<=397\'\'scl\'" % c_sq503_label, '', 0, '0:' + str(c_afternoon), 0)
    
    if time > datetime.time (18,0):
        G.marker ("@ysq75\'i\\=1\'=13\'scl\'\\fff\'c", '', 0, '0:' + str(c_sq503), 0)
        G.marker ("@y%s\'h\\=10\'f\\fff\'c\\h-0-10\'a\\<=132\'\'scl\'" % c_sq504_label, '', 0, '0:' + str(c_evening), 0)    
    
    G.marker ("@yl\'h\\=18\'f\\" + color_marker + "\'c\\l-0-13\'a", '', 0, '0:' + str(c_label), 0) # adds emphasis marker
    text = "@y" + str(round(current_sum,1)) + " kWh used\'h\\=10\'f\\" + color_marker + "\'c\\-6-10\'a"
    G.marker (text, '', 0, '0:' + str(c_label), 0)

# HISTORICAL
    if date.year == now.year and date.month == now.month and date.day == now.day:
        G.marker (r"@ysq'i\=" + str(b_length) + r"'=13'scl'\c0c0c0'c", '', 0, '0.5:0', 0, -1) # controls length of historical light gray area
    G.marker (r"@ynight'h\=10'f\fff'c\h-0-10'a\<=67''scl'", '', 0, '0.5:' + str(b_night), 0) # adds 'night'
    G.marker (r"@ysq50'i\=1'=13'scl'\fff'c", '', 0, '0.5:' + str(b_sq501), 0) # adds night divider
    G.marker (r"@ymorning'h\=10'f\fff'c\h-0-10'a\<=220''scl'", '', 0, '0.5:' + str(b_morning), 0) # adds 'morning' 
    G.marker (r"@ysq50'i\=1'=13'scl'\fff'c", '', 0, '0.5:' + str(b_sq502),0) # adds morning divider
    G.marker (r"@yafternoon'h\=10'f\fff'c\h-0-10'a\<=397''scl'", '', 0, '0.5:' + str(b_afternoon), 0) # adds 'afternoon' 
    G.marker (r"@ysq50'i\=1'=13'scl'\fff'c", '', 0, '0.5:' + str(b_sq503), 0) # controls historical afternoon divider
    G.marker (r"@yevening'h\=10'f\fff'c\h-0-10'a\<=181''scl'", '', 0, '0.5:' + str(b_evening), 0) # adds 'evening'
    G.marker (r"@yl'h\=18'f\666666'c\l-0-13'a", '', 0, '0.5:' + str(b_label), 0) # adds emphasis marker on historical
    text = r"@y" + str(round(historical_total,1)) + r" kWh expected'h\=10'f\666666'c\-6-10'a"
    G.marker (text, '', 0, '0.5:' + str(b_label), 0)

    ### debug
    debug = []
    debug.append ("date: %s, time: %s" % (date, time))
    #print "diff: ", diff.days, diff.seconds
    debug.append ("current: %s, historical(sum): %s, historical (total): %s, max: %s: " % (current_sum, historical_sum, historical_total, kw_max))
    debug.append ("current data: %s" % (current))
    debug.append ("budget data: %s" % (budget))
    debug.append ("percentage: %s" % (percentage))
    
    #print ": %s" %()
    debug.append ("c_max: %s, b_max: %s" %(c_max, b_max))
    debug.append ("b_length: %s" %(b_length))
    debug.append ("c_label: %s, b_label: %s" %(c_label, b_label))
    debug.append ("c_sq501: %s, b_sq501: %s" %(c_sq501, b_sq501))
    debug.append ("c_sq502: %s, b_sq502: %s" %(c_sq502, b_sq502))
    debug.append ("c_sq503: %s, b_sq503: %s" %(c_sq503, b_sq503))
    #print ": %s, : %s" %()
    #print ": %s, : %s" %()
    ### debug

    
    

    return [str(G), percentage, debug]

def CreateDayChart():

    G = VerticalBarStack(['CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC________________________________________________________________________________________________________________________________________________,BAABAAAAABAAAAABAAAAAAAAAAAAAAABIgmXECBBBABCCCLSBAAAAAAABBBBAABHTBBABBABABBABCHHCBCCENBAABAABBEIQDOAABABFIHEEABBABBACBBCBFieBBCABDDCCBABBBAACBCA________________________________________________________________________________________________________________________________________________', 
                                '________________________________________________________________________________________________________________________________________________CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC___________________________________________________,________________________________________________________________________________________________________________________________________________BBCABBAABBAABAABAABBAABABBAABCABBABBABWACBBWBDBCPxqFFVeDTLYFUBBABBABBABBABMNJEEoLTFfCBCBABAAA___________________________________________________'], 
                                encoding='simple')

    G.color('8bbc8b', 'b4e4b4', '1d7f1d', '70d070')
    G.size(1000,150)
    G.axes('xr')
    G.axes.position(0,0,12.5,25,37.5,50,62.5,75,87.5,100) #chxp
    G.axes.label(0,'12a','6a','12p','6p','12a','6a','12p','6p','12a' )#chxl
    G.axes.style(0,'666666',10,0,'lt','ffffff') #chxs
    G.axes.style(1,'666666',10,-1,'t','ffffff')
    G.axes.tick(0,2) #chxtc
    G.axes.tick(1,2)
    G.orientation(0)#chp
    G.grid(12.5,20,0.25,0.75)#chg
    G.bar('a',0,0) #chbh
    G.marker('@telectricity in kW','666666',0,'1:1',10) #chm
    G.marker('B','b4e4b4',1,0,0)
    G.marker('B','8bbc8b',0,0,0)
    G.marker('B','70d070',3,0,0)
    G.marker('B','1d7f1d',2,0,0)
    #G.fill('c','s','f8f8f8',0.5) #chf
    #G.fill('c','s','ffffff',0.5) 
    G.margin(10,20,0,0) #chma
    return str(G)
    
    
def CreateDayChart2(request, year, month, day):

    now = datetime.datetime.now() + datetime.timedelta(hours=-7)

    year = int(year)
    month = int(month)
    day = int(day)
    
    start = datetime.datetime(year, month, day)    
    end = start.replace(hour = 23)
        
    hour_start = start.replace (hour=now.hour)
    
    data = []
    
    for hour in range (0, 24):
        date = start.replace(hour=hour)
        data.append({'POWER' : 0, 'DATE' : date})
        
    colors = ['b4ecb4'] * 24
    
    if year == now.year and month == now.month and day == now.day:
        # Django Development command...
        # hour_sum = TED_history_minute.objects.raw('SELECT sum(POWER) FROM TED_history_minute WHERE DATE >= %s', [hour_start])
        
        # Django 1.1 command...
        cursor = connection.cursor()
        cursor.execute("SELECT sum(POWER) FROM TED_history_minute WHERE DATE >= %s", [hour_start])
        hour_sum = cursor.fetchone()[0]
        # end
    
        if hour_sum:
            data[hour_start.hour] = {'POWER' : hour_sum/60, 'DATE' : hour_start}
            colors[hour_start.hour] = '70d070'
            
    history = TED_history_hour.objects.filter(DATE__gte=start)
    history = history.filter(DATE__lte=end)
    history = history.order_by('DATE')
    
    budget = [2.464, 10.061, 7.433, 12.693]
    current = [0.0, 0.0, 0.0, 0.0]
    
    for item in list(history):
        # insert history in data...
        hour = item.DATE.hour
        data[hour] = {'POWER' : item.POWER, 'DATE' : item.DATE}
        
        # group power for budget chart...
        if hour < 6:
            # add to night
            current[0] += float(item.POWER)
        elif hour < 12:
            # add to morning
            current[1] += float(item.POWER)
        elif hour < 18:
            # add to afternoon
            current[2] += float(item.POWER)
        elif hour < 23:
            # add to evening
            current[3] += float(item.POWER)
    
    budgetchart = CreateDayBudgetChart (end, current, budget)

    G = VerticalBarStack(data, encoding='text')

    G.size(1000,150)
    G.axes('xr')
    
    print str(G)

    return render_to_response ('electric/bar_day.html', {'data' : data, 'date' : start, 'colors' : string.join(colors, '|'), 'budgetchart': budgetchart}, context_instance=RequestContext(request))
    

    
    

def bar_jumps(request, year, month, day):
    return

    now = datetime.datetime.now() + datetime.timedelta(hours=-7)

    year = int(year)
    month = int(month)
    day = int(day)
    
    start = datetime.datetime(year, month, day)    
    end = start.replace(hour = 23)
    
    start = start - datetime.timedelta(hours=24)
    data = {}
    colors = ['b4ecb4']
    
    # work on second chart for the day...
    
    history = TED_history_second.objects.filter(DATE__gte=start-datetime.timedelta(days=1))
    history = history.filter(DATE__lte=end)
    history = history.order_by('DATE')

    oldpower = 0
    newpower = 0
    olddate = datetime.datetime(2000, 1, 1)
    class PowerClass: 
        pass
    
    #i = 0    
    
    for item in list(history):
        #i += 1
        newdate = item.DATE
        newpower = item.POWER
        if newdate - olddate == datetime.timedelta(seconds=1):
            if oldpower != 0:
                diff = newpower - oldpower
                if abs(diff) > 1 and not data.has_key(abs(diff)):
                    value = [0, 0]
                    data[abs(diff)] = value
                elif abs(diff) > 1:
                    value = data.get(abs(diff))
                    
                if diff > 1:
                    up = value[0] + 1
                    down = value[1]    
                    data[abs(diff)] = [up, down]
                elif diff < -1:
                    up = value[0]
                    down = value[1] - 1    
                    data[abs(diff)] = [up, down]
                    
        olddate = newdate
        oldpower = newpower
    
    
    title = "Electricity use for %s" % (start.strftime('%B %d %Y'))
    
    return render_to_response ('electric/bar_jumps.html', {'data' : data, 'title' : title, 'colors' : string.join(colors, '|')}, context_instance=RequestContext(request))

def timeline_min(request):
    
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    delta = datetime.timedelta (days=1)
    start = now - delta

    data = TED_history_minute.objects.filter(DATE__gte=start)
    data = data.order_by('-DATE')    
    
    title = "Timeline (Minute)"
    
    #objects = get_object_or_404 (TED_history_second, DATE>=start)
    return render_to_response ('electric/timeline.html', {'title' : title, 'data' : data, 'start' : start, 'end' : now}, context_instance=RequestContext(request))

def timeline_hour(request):

    max = 14 # in days
    
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    delta = datetime.timedelta (days=max)
    start = now - delta

    data = TED_history_hour.objects.filter(DATE__gte=start)
    data = data.order_by('-DATE')
    
    title = "Timeline (Hour)"
    #objects = get_object_or_404 (TED_history_second, DATE>=start)
    return render_to_response ('electric/timeline.html', {'title' : title, 'data' : data, 'start' : start, 'end' : now}, context_instance=RequestContext(request))

def timeline_day(request):

    max = 365 # in days
    
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    delta = datetime.timedelta (days=max)
    start = now - delta

    data = TED_history_day.objects.filter(DATE__gte=start)
    data = data.order_by('-DATE')
    
    title = "Timeline (Day)"
    return render_to_response ('electric/timeline.html', {'title' : title, 'data' : data, 'start' : start, 'end' : now}, context_instance=RequestContext(request))


def bar_sec(request):

    max = 60 * 60# three hours
    data = TED_history_second.objects.all().order_by('-DATE')[:max]


    #objects = get_object_or_404 (TED_history_second, DATE>=start)
    return render_to_response ('electric/bar.html', {'data' : data}, context_instance=RequestContext(request))

def bar_min(request):

    max = 60 *5 # two days
    data = TED_history_minute.objects.all().order_by('-DATE')[:max]
    data.reverse()
    #objects = get_object_or_404 (TED_history_second, DATE>=start)
    return render_to_response ('electric/bar.html', {'data' : data}, context_instance=RequestContext(request))

def bar_hour(request):

    now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    start = datetime.datetime(now.year, now.month, now.day, now.hour)
    

    data = TED_history_second.objects.filter(DATE__gte=start)
    data = data.order_by('DATE')
    
    colors = ['b4ecb4']
    #['84c984'] + ['b4ecb4'] * 5 + ['84c984']
    
    title = "Week of %s" % (start.strftime('%B %d %Y'))
    
    return render_to_response ('electric/bar_day.html', {'data' : data, 'title' : title, 'colors' : string.join(colors, '|')}, context_instance=RequestContext(request))

def overview(request):
    
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    delta = datetime.timedelta (hours=1)
    start = now - delta
    
    data1 = TED_history_second.objects.filter(DATE__gte=start)
    #second_data = data.order_by('-DATE')
    
    data2 = TED_history_minute.objects.filter(DATE__lt=start)
    #data = data.order_by('-DATE')
    
    title = "Timeline (Overview)"
        
    #objects = get_object_or_404 (TED_history_second, DATE>=start)
    return render_to_response ('electric/timeline.html', {'title' : title, 'data' : data1, 'data2' : data2, 'start' : start, 'end' : now}, context_instance=RequestContext(request))
