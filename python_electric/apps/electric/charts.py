import datetime, string
from GChartWrapper import *
from settings import CHART
from decimal import *

# 
import os
os.environ['HOME'] = "/home/spaceriqui/svn/python_electric/media/charts"

# do this before importing pylab or pyplot
import matplotlib
matplotlib.use('Agg')
import pylab as plt
from matplotlib.dates import HourLocator, DateFormatter


##import logging, logging.config
##
##logging.config.fileConfig("logging.conf")
##log = logging.getLogger("python_electric.charts")

## colors... top b4ecb4 5a9f59 bottom (84c984 extra for weekends), top 70d070, 1d7f17 bottom 

# top opaque light green on historical data
lightgreenold = 'b4ecb4'
# bottom opaque dark green on historical data
darkgreenold = '5a9f59'
# top bright light green on current data
lightgreencurrent = '70d070'
# bottom bright dark green on current data
darkgreencurrent = '1d7f17' #'229a1c' # was '1d7f17'

current = '155811'#'1d7f17'

plotline = current#'8B0000'
lightgrey = 'D3D3D3'

chartcolor = '#afafaf'
textcolor = '#6e6e6e'

width = CHART.WIDTH

def CreateDayHourChart (start, data):
  
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    x = []
    d = []
    mx = Decimal(CHART.Y_MAX)
    y_max = 4095
    x_label = ['12a', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                '12p', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

    color = []

##    print "mx: %s (%s)" % (mx, type(mx))
            
    for item in data:
        power = item['POWER']
        date = item['DATE']
        
        x.append(float(power))
        d.append(date)
        
        if power == 0:
            pass
        else:
            if power > mx:
                mx = power
                
        if date.year == now.year and date.month == now.month and date.day == now.day and date.hour == now.hour:
            color.append (current)
        else:
            color.append (lightgreencurrent)
    
    bottom = 0
    top = int(float(mx)+float(0.999999999999))
    
##    print "mx: %s (%s)" % (mx, type(mx))
##    print "bottom: %s top: %s" % (bottom, top)
    
    scale = y_max/(top-bottom)
    
    for i in range (0, len(x)):
        x[i] = x[i] * scale
        if x[i] > y_max:
##            print "Error: x[%s]=%s is greater than %s.  Scale of %s is wrong!" % (i, x[i], y_max, scale)
            x[i] = y_max
    
   
    G = VerticalBarStack([x], encoding='extended')
    G.color('|'.join(color))

    G.size(width,150)
    G.margin(0,0,10,10)
    
    G.axes('xyr') 

    cost = 0.08

    G.axes.range(1, round(bottom*cost,2),round(top*cost,2),round(cost,2))
    G.axes.range(2, bottom,top,1)
    
    G.axes.label(0, '|'.join(x_label))
    
    # bar thickness and spacing
    G.bar('r', 0.1, 0.1)
    
    G.grid(0, 99.9/(top-bottom), 1, 0)
    
    # electricity in kW label
    G.marker ('@telectricity in kW h', '666666', 0, '1:1', 10)
    G.marker ('@telectricity in $', '666666', 0, '0:1', 10)
    
    return str(G)


def CreateWeekDayChart (data):
    
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)

    x = []
    d = []
    mx = Decimal(CHART.Y_MAX)
    y_max = 4095
    x_label = []
    color = []

##    print "WeekDayChart mx: %s (%s)" % (mx, type(mx))
            
    for item in data:
        power = item['POWER']
        date = item['DATE']
        
        x.append(float(power))
        x_label.append(date.strftime('%a-')+str(date.day))
        
        if date.year == now.year and date.month == now.month and date.day == now.day:
            color.append (current)
        elif date.strftime('%U') == now.strftime('%U'):
            if date.strftime('%w') in ['0','6']:
                color.append (darkgreencurrent)
            else:
                color.append (lightgreencurrent)
        elif date.strftime('%w') in ['0','6']:
            color.append (darkgreenold)
        else:
            color.append (lightgreenold)
     
        if power == 0:
            pass
        else:
            if power > mx:
                mx = power
        
##    print "WeekDayChart mx: %s (%s)" % (mx, type(mx))
    
    #print x
    #print x_label
    
    bottom = 0
    
    top = (int(mx/10)+1)*10
    if (top - bottom) >= 40:
        step = 10
    elif (top - bottom) >= 20:
        step = 5
    elif (top - bottom) >= 10:
        step = 2
    else:
        step = (int(mx/10)+1)*2

    #print "WeekDayChart bottom: %s top: %s step: %s" % (bottom, top, step)
    
    scale = y_max/(top-bottom)

    
##    print "WeekDayChart scale: %s" % scale    
    for i in range (0, len(x)):
        x[i] = x[i] * scale
        if x[i] > y_max:
            print "Error: x[%s]=%s is greater than %s.  Scale of %s is wrong!" % (i, x[i], y_max, scale)
    
   
    G = VerticalBarStack([x], encoding='extended')

    G.color('|'.join(color))

    G.size(width,150)
    G.margin(0,0,10,10)
    
    G.axes('xyr') 

    cost = 0.08

    G.axes.range(1, round(bottom*cost,2),round(top*cost,2),round(step*cost,2))
    G.axes.range(2, bottom,top,step)
    
    G.axes.label(0, '|'.join(x_label))
    
    # bar thickness and spacing
    G.bar('r', 0.1, 0.1)
    
##    print "WeekDayChart grid: %s" % (99.9/(top-bottom))
    G.grid(0, 99.9/(top-bottom)*step, 1, 0)
    
    # electricity in kW label
    G.marker ('@telectricity in kW h', '666666', 0, '1:1', 10)
    G.marker ('@telectricity in $', '666666', 0, '0:1', 10)
    
    return str(G)

def CreateWeekScatterChart (data):

   
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    x = []
    d = []
    mx = 0
    x_label = ['','12a','1','2','3','4','5','6','7','8','9','10','11','12p','1','2','3','4','5','6','7','8','9','10','11','']
    y_label = ['','Sun','Mon','Tue','Wed','Thr','Fri','Sat','']
    color = []
    dotsize = int(25.0*width/600)
    chd_1 = []
    for i in range (0,24):
        chd_1.append(str(i))
    chd_1 = chd_1 * 8
    chd_2 = []
    for i in range (0,8):
        for k in range (0,24):
            chd_2.append(str(i))
    chd_3 = ['0.0']*24*8 # *8 for an extra row of zeros

##    max_x = 0
##    max_x = 0
    for item in data:
        power = item['POWER']
        date = item['DATE']
        
        x.append(float(power))
        
        if date.year == now.year and date.month == now.month and date.day == now.day:
            if date.hour == now.hour:
                color.append (current)
            else:
                color.append (lightgreencurrent)
        else:
            color.append (lightgreenold)
     
        if power > mx:
            mx = power
        
    #print "mx: %s (%s)" % (mx, type(mx))
    #print x
    #print x_label
    #print "bottom: %s top: %s" % (bottom, top)

    if mx == 0:
         scale = 0
    else:
         scale = float(dotsize/mx)
    
    #print dotsize
    #print scale, type(scale)

    
    for i in range (0, len(x)):
        #print x[i], type(x[i])
        chd_3[i] = str(int(round(x[i] * scale, 0)))

    G = Scatter([chd_1, chd_2, chd_3], encoding='text')

##    G.color('|'.join(color))

    G.size(width,width/3)

    G.scale (-1,24,-1,7,0,int(dotsize*.75))
    G.axes('xy')
    G.marker('o',darkgreenold,1,-1,dotsize)
    G.axes.label(0, '|'.join(x_label))
    G.axes.label(1, '|'.join(y_label))
    
    #G.color('|'.join(color))

    # electricity in kW label
    G.marker ('@tmax ' + str(round(mx,1)) + 'kW h', '666666', 0, '1:1', 10,1)

    return str(G)    


def CreateMonthDayChart (data):
    
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)

    x = []
    d = []
    mx = Decimal(CHART.Y_MAX)
    y_max = 4095
    x_label = []
    color = []

    #print "mx: %s (%s)" % (mx, type(mx))
            
    for item in data:
        power = item['POWER']
        date = item['DATE']
        
        x.append(float(power))
        x_label.append(str(date.day))
        
        if date.year == now.year and date.month == now.month and date.day == now.day:
            color.append (current)
        elif date.strftime('%w') in ['0','6']:
            color.append (darkgreencurrent)
        else:
            color.append (lightgreencurrent)
     
        if power == 0:
            pass
        else:
            if power > mx:
                mx = power
        
    #print "mx: %s (%s)" % (mx, type(mx))
    
    #print x
    #print x_label
    
    bottom = 0
#    top = int(float(mx)+float(0.99))
    top = (int(mx/10)+1)*10
    step = (int(mx/10)+1)*2
    
##    print "MonthDay Chart bottom: %s top: %s" % (bottom, top)
    
    scale = float(y_max/(top-bottom))
    
##    print "MonthDay Chart scale: %s" % scale    
    for i in range (0, len(x)):
        x[i] = x[i] * scale
        if x[i] > y_max:
            print "Error: x[%s]=%s is greater than %s.  Scale of %s is wrong!" % (i, x[i], y_max, scale)
    
   
    G = VerticalBarStack([x], encoding='extended')

    G.color('|'.join(color))

    G.size(width,150)
    G.margin(0,0,10,10)
    
    G.axes('xyr') 

    cost = 0.08

    G.axes.range(1, round(bottom*cost,2),round(top*cost,2),round(step*cost,2))
#    G.axes.range(1, bottom,top,step)
    G.axes.range(2, bottom,top,step)
    
    G.axes.label(0, '|'.join(x_label))
    
    # bar thickness and spacing
    G.bar('r', 0.1, 0.1)
    
    #print "grid: %s" % (100.0/(top-bottom))
    G.grid(0, 99.9/(top-bottom)*step, 1, 0)
        
    # electricity in kW label
    G.marker ('@telectricity in kW h', '666666', 0, '1:1', 10)
    G.marker ('@telectricity in $', '666666', 0, '0:1', 10)
    return str(G)

def CreateYearMonthChart (data):
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    
    x = []
    x2 = []
    d = []
    mx_1 = Decimal(CHART.Y_MAX)
    mx_2 = Decimal(CHART.Y_MAX)
    mn_2 = Decimal(10000000)
    
    y_max = 4095.0
    x_label = []
    color = []

    #print "mx_1: %s (%s)" % (mx_1, type(mx_1))
            
    for item in data:
        power = item['POWER']
        date = item['DATE']
        average = item['AVERAGE']
        
        x.append(float(power))
        x2.append(float(average))
        x_label.append(date.strftime('%b'))
        
        if date.year == now.year and date.month == now.month:
            color.append (current)
        else:
            color.append (lightgreenold)
     
        if power == 0:
            pass
        else:
            if power > mx_1:
                mx_1 = power
        
        if average == 0:
            pass
        else:
            if average > mx_2:
                mx_2 = average
            if average < mn_2:
                mn_2 = average
        
    bottom_1 = 0
    top_1 = (int(mx_1/100)+1)*100
    scale_1 = y_max/(top_1-bottom_1)
    step_1 = (int((top_1-bottom_1)/10))*2
    
##    print "YearMonth bottom_1: %s" % bottom_1
##    print "YearMonth top_1: %s" % top_1
##    print "YearMonth scale_1: %s" % scale_1
##    print "YearMonth step_1: %s" % step_1
    

    bottom_2 = (int(mn_2/10))*10
    top_2 = (int(mx_2/10)+1)*10
    scale_2 = y_max/(top_2-bottom_2)
    step_2 = (int((top_2-bottom_2)/10))*2

##    print "YearMonth bottom_2: %s" % bottom_2
##    print "YearMonth top_2: %s" % top_2
##    print "YearMonth scale_2: %s" % scale_2
##    print "YearMonth step_2: %s" % step_2

    grid=100.0/(top_1-bottom_1)*step_1
##    print "YearMonth grid: %s" % grid
    
    # used to only display the averages for which it is > 0
    x2_end = len(x2)
    x2_start = x2_end
    
    for i in range (0, len(x)):
        x[i] = x[i] * scale_1
        if x2[i] <> 0:
            x2[i] =(x2[i]-bottom_2) * scale_2
            if i < x2_start: x2_start = i
        if x[i] > y_max:
            print "Error: x[%s]=%s is greater than %s.  scale_1 of %s is wrong!" % (i, x[i], y_max, scale_1)
        if x2[i] > y_max:
            print "Error: x2[%s]=%s is greater than %s.  scale_2 of %s is wrong!" % (i, x2[i], y_max, scale_2)
    
    G = VerticalBarStack([x,x2], encoding='extended', series=1)
    G.marker ('D', 'darkred', 1, '%s:%s'%(x2_start, x2_end), 1)

    G.color('|'.join(color))

    G.size(width,150)
    G.margin(0,0,10,10)
    
    G.axes('xyr') 

    G.axes.range(1, bottom_1,top_1,step_1)
    G.axes.range(2, bottom_2,top_2,step_2)
##    G.axes.range(1, bottom_1,top_1,(top_1-bottom_1)/4)
##    G.axes.range(2, bottom_2,top_2,(top_2-bottom_2)/4)
    G.axes.label(0, '|'.join(x_label))
    
    # bar thickness and spacing
    G.bar('r', 0.1, 0.1)
    
    G.grid(0, grid, 1, 0)
    
    # electricity in kW label
    G.marker ('@taverage in kW h/day', '666666', 0, '1:1', 10)
    G.marker ('@ttotal in kW h', '666666', 0, '0:1', 10)

    return str(G)
    
    
def CreateDayBudgetChart (date, current, budget):
    
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)


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
        
    if c_sq502-c_sq501 > 0.06:
        c_sq502_label = 'morning'
    elif c_sq502-c_sq501 > 0.03:
        c_sq502_label = 'mor.'
    else:
        c_sq502_label = ''

    if c_sq503-c_sq502 > 0.08:
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

    return [str(G), percentage]
    



def CreateWeeklyBudgetChart (year, week, current, budget):
     
    now = datetime.datetime.now() + datetime.timedelta(hours=-7)

    year_start = datetime.datetime(year, 1, 1)
    week0 = year_start - datetime.timedelta(days=year_start.isoweekday())
    start = week0 + datetime.timedelta(weeks=week)
    
    if year == now.year and week == int(now.strftime('%U')):
        end = now
    else:
        end = start + datetime.timedelta(weeks=1) - datetime.timedelta(seconds=1)
        
    #print "start: %s, end: %s" % (start, end)
    
    current_sum = 0.0
    for i in current:
        current_sum += i
        #print "current: %s, current(sum):%s" % (i, current_sum)
    
    historical_total = 0.0
    for i in budget:
        historical_total += i
        #print "budget: %s, historical(total):%s" % (i, historical_total)
        
    kw_max = max(current_sum, historical_total)

    diff = end - start
    #i = diff.days + diff.seconds/float(60*60*24)

    historical_sum = 0.0

    for i in range(0,diff.days):
        historical_sum += budget[i]
        #print "budget [%s]: %s, historical(sum): %s" %(i, budget[i], historical_sum)
    
    if diff.days < 7:
        historical_sum += budget[diff.days]*diff.seconds/float(60*60*24)
        #print "fraction: %s, +kW: %s, historical(sum): %s" %(diff.seconds/float(60*60*24), budget[diff.days]*diff.seconds/float(60*60*24), historical_sum)
    
    percentage = (current_sum - historical_sum) / historical_sum
        

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


    regions = 7
    precision = 3

    c_max =  1/float(kw_max)
    #pixel_max = 900
    #pixel_max = width - 1000
    c_label = current_sum/historical_total
    if c_label > 1:
        c_label = 1.0
    
    b_max =  historical_total/float(kw_max)
##    print "b_max: %s" % b_max
    b_label = b_max
    #pixel_max = 865
    pixel_max = width - 145
##    print "b_label: %s (%s)" % (b_label, b_label*pixel_max)
    #b_length = long(pixel_max*b_max)
    b_length = (pixel_max-20) * b_max +20
##    print "b_length: %s" % b_length

    c_sq = [0]*regions
    c_l = [0]*regions
    b_sq = [0]*regions
    b_l = [0]*regions
    
    for i in range (0, regions):
        for j in range (0,i+1):
            c_sq[i] += current[j]
            b_sq[i] += budget[j]
        c_sq[i] = round(c_sq[i] * c_max, precision)
        b_sq[i] = round(b_sq[i] * b_max / historical_total, precision)
        if i > 0:
            c_l[i] = round((c_sq[i] - c_sq[i-1])/2 +  c_sq[i-1], precision)
            b_l[i] = round((b_sq[i] - b_sq[i-1])/2 +  b_sq[i-1], precision)
        else:
            c_l[i] = round(c_sq[i]/2, precision)
            b_l[i] = round(b_sq[i]/2, precision)
        

    ### debug
##    print "current: %s, budget: %s" % (current, budget)
##    print "start, end", start, end
##    print "diff: ", diff.days, diff.seconds
##    print "current: %s, historical(sum): %s, historical (total): %s, max: %s: " % (current_sum, historical_sum, historical_total, kw_max)
##    print "percentage: %s" % (percentage)
##    print "c_max: %s" % (c_max)
##    for i in range (0, regions):
##        print c_sq[i], c_l[i], b_sq[i], b_l[i]
        
    ### debug
    
    # Set budget chart paramaters

    # cht=bhs
    # chd=e:ySAA,AA1Z
    G = HorizontalBarStack([ [current_sum/kw_max * 100],[0,historical_sum/kw_max * 100] ], encoding='text') 
    
    # chs=425x34
    G.size(width,34)

    # chco=70d070,666666
    G.color(color, '666666')
    
    ## chma=10,0
    G.margin(20,0,0,0)

    # chbh=13,1,1
    G.bar(13,1,1)
    
    # chxt=x,y,r
    G.axes('xyr')
    
    # chxl=2:
    #     210+kW%C2%B7h+expected
    #     160+kW%C2%B7h+used
    G.axes.label(2, str(historical_total) + ' kWh expected', str(current_sum) + ' kWh used')
    
    # chxs=0,ffffff,0,0,t
    #     1,ffffff,10,1,t
    #     2,ffffff,10,-1,t,ffffff
    G.axes.style(0,'ffffff',0,0,'t')
    G.axes.style(1,'ffffff',10,1,'t')
    G.axes.style(2,'ffffff',10,-1,'t','ffffff')
    
    # chxtc=0,0
    #     1,0
    #     2,6
    G.axes.tick(0,0)
    G.axes.tick(1,0)
    G.axes.tick(2,6)    
    
    # Current
    
    #     @ysq'i\=999'=13'scl'\fff'c,,0,0.5:1,0,-1
    

    # Current... 
    # Labels for days of the week.
    #     @yS'h\=10'f\fff'c\h-0-10'a,,0,0:0.096,0
    
    min_space = 0.03

    G.marker ("@yS\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[0]), 0)
    if c_sq[1]-c_sq[0] > min_space:
        G.marker ("@yM\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[1]), 0)
    if c_sq[2]-c_sq[1] > min_space:
        G.marker ("@yT\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[2]), 0)
    if c_sq[3]-c_sq[2] > min_space:
        G.marker ("@yW\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[3]), 0)
    if c_sq[4]-c_sq[3] > min_space:
        G.marker ("@yT\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[4]), 0)
    if c_sq[5]-c_sq[4] > min_space:
        G.marker ("@yF\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[5]), 0)
    if c_sq[6]-c_sq[5] > min_space:
        G.marker ("@yS\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[6]), 0)

    #    @yl'h\=18'f\a06000'c\l-0-13'a,,0,0:0.152,0
    G.marker ("@yl\'h\\=18\'f\\" + color_marker + "\'c\\l-0-13\'a", '', 0, '0:' + str(round(c_label,precision)), 0) # adds emphasis marker   
    
    # bar label for kwh used
    #     @y160+kW%C2%B7h+used'h\=10'f\008000'c\-6-10'a,,0,0:0.786,0
    text = "@y" + str(round(current_sum,1)) + " kWh used\'h\\=10\'f\\" + color_marker + "\'c\\-6-10\'a"
    G.marker (text, '', 0, '0:' + str(round(c_label, precision)), 0)

    
    for i in range (0, regions):
        if i < int(end.strftime('%w')):
            # Current...
            #     @ysq75'i\=1'=13'scl'\fff'c,,0,0:0.192,0
            G.marker ("@ysq75\'i\\=1\'=13\'scl\'\\fff\'c", '', 0, '0:' + str(c_sq[i]), 0)    
        
        # Budget...
        #     @ysq50'i\=1'=13'scl'\fff'c,,0,0.5:0.177,0
        G.marker ("@ysq50\'i\\=1\'=13\'scl\'\\fff\'c", '', 0, '0.5:' + str(b_sq[i]), 0)    


    
    # Budget... Days of the week
    #     @yS'h\=10'f\fff'c\h-0-10'a,,0,0.5:0.089,0
    G.marker ("@yS\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[0]), 0)
    G.marker ("@yM\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[1]), 0)
    G.marker ("@yT\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[2]), 0)
    G.marker ("@yW\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[3]), 0)
    G.marker ("@yT\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[4]), 0)
    G.marker ("@yF\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[5]), 0)
    G.marker ("@yS\'h\\=10\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[6]), 0)
    
    # historical light gray area...
    # chm=@ysq'i\=999'=13'scl'\c0c0c0'c,,0,0.5:0,0,-1
    if year == now.year and week == int(now.strftime('%U')):
        G.marker (r"@ysq'i\=" + str(b_length) + r"'=13'scl'\c0c0c0'c", '', 0, '0.5:0', 0, -1) # controls length of historical light gray area    
    
    
    #    @yl'h\=18'f\666666'c\l-0-13'a,,0,0.5:1,0
    G.marker (r"@yl'h\=18'f\666666'c\l-0-13'a", '', 0, '0.5:' + str(round(b_label,precision)), 0) # adds emphasis marker on historical
    
    # historical bar label for kwh used
    #     @y210+kW%C2%B7h+expected'h\=10'f\666666'c\-6-10'a,,0,0.5:1,0
    text = r"@y" + str(round(historical_total,1)) + r" kWh expected'h\=10'f\666666'c\-6-10'a"
    G.marker (text, '', 0, '0.5:' + str(round(b_label, precision)), 0)

    return [G.url, percentage]

def CreateAverageChart (data):
    
    mx = 0
    mn = 1000
    count = 0
    y_max = 4095
    #y_max = 100
    
    x_label = []

    now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    
    for item in data:
        d, x1, x2, x3, x4 = item
        count += 1
        for y in [x1, x2, x3, x4]:
            if y == 0:
                pass
            else:
                if y > mx:
                    mx = y
                if y < mn:
                    mn = y
        if int(d.strftime('%w')) == 0:
            x_label.append (d.strftime('%m-%d'))
        else:
            x_label.append (" ")
            
        
    
    if len(data) > 0:
         d, x1, x2, x3, x4 = zip(*data)
    else:
         return ""
    
    count = len(d)  
    
    bottom = int(mn/10)*10
    top = (int(mx/10)+1)*10
    
    scale = y_max/(top-bottom)
    d_start = d[0]
    d_end = d[count-1]
    
##    print d_end
    
    x1=list(x1)
    x2=list(x2)
    x3=list(x3)
    x4=list(x4)
    
    y1 = [0]*count
    y2 = [0]*count
    y3 = [0]*count
    y4 = [0]*count
    
    
    for i in range(0, count):
        if x1[i] > 0:
            y1[i] = round((x1[i]-bottom)*scale,1)
        else:
            y1[i] = None
        if x2[i] > 0:
            y2[i] = round((x2[i]-bottom)*scale,1)
        else:
            y2[i] = None
        if x3[i] > 0:
            y3[i] = round((x3[i]-bottom)*scale,1)
        else:
            y3[i] = None
        if x4[i] > 0:
            y4[i] = round((x4[i]-bottom)*scale,1)
        else:
            y4[i] = None

    #G = Line([y1, y2, y3, y4], encoding='extended')
    #G.color('c0c0c0', 'lightgreen', 'lightblue', 'darkred')
    #G.legend('7 day','14 day','21 day','28 day')


    G = Line([y1, y4], encoding='extended')
    G.color(lightgrey, plotline)
    G.legend('7 day','28 day')
    G.legend_pos('b')

    G.size(width,300)
    G.margin(0,0,10,10)
    
    cost = 0.08

    G.axes('xyr') 
    G.axes.range(1, cost*bottom,cost*top,cost*2)
    G.axes.range(2, bottom,top,4)
    
    G.axes.label(0, '|'.join(x_label))

    dayofweek = int(d_start.strftime('%w'))
    x_stepsize = 99.9/(count-1)*7
    y_stepsize = y_max/scale/2
    x_offset = x_stepsize - dayofweek/7.0*x_stepsize
 
    G.grid(x_stepsize, y_stepsize, 1, 0, x_offset, 0)
    
    G.marker ('@telectricity in kW h', '666666', 0, '1:1', 10)
    G.marker ('@telectricity in $', '666666', 0, '0:1', 10)

    return str(G)

    
def CreateDayDetailChart (date,timedata, kwdata):
    matplotlib.rcParams['figure.figsize'] = '8, 2'
    matplotlib.rcParams['font.size'] = 8.5 # 12.0
    matplotlib.rcParams['font.family'] = 'arial' # sans-serif
    matplotlib.rcParams['text.color'] = 'orange'#textcolor # black
    matplotlib.rcParams['axes.edgecolor'] = chartcolor # axes edge color (black)
    matplotlib.rcParams['xtick.color'] = textcolor#'red'#chartcolor
    matplotlib.rcParams['ytick.color'] = textcolor#'yellow'#chartcolor
    matplotlib.rcParams['grid.color'] = chartcolor
    matplotlib.rcParams['lines.color'] = plotline
    matplotlib.rcParams['lines.linewidth'] = 0.6

    #matplotlib.font_manager.FontProperties(family=None, style=None, variant=None, weight=None, stretch=None, size=None, fname=None, _init=None)
    #matplotlib.font_manager.FontProperties(stretch='expanded')
    
    hours = HourLocator() # Every Hour
    
    # figure 1 small
    
    filename = CHART.PATH + date.strftime('%Y%m%d-small.png')
    hoursFmt = DateFormatter('%I')
    fig = plt.figure()
    fig.subplots_adjust(left=0.023)
    fig.subplots_adjust(right=0.978)
    ax = fig.add_subplot(111)
    ax.plot(timedata,kwdata,)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(hoursFmt)
    ax.autoscale_view()
    fig.savefig(filename)
    
    # figure 2 large
    filename = CHART.PATH + date.strftime('%Y%m%d.png')
    matplotlib.rcParams['figure.figsize'] = '75, 6'
    matplotlib.rcParams['lines.linewidth'] = 0.5

    hoursFmt = DateFormatter('%I:00 %p')
    fig2 = plt.figure()
    fig2.subplots_adjust(left=0.01)
    fig2.subplots_adjust(right=0.99)
    ax = fig2.add_subplot(111)
    ax.plot(timedata,kwdata)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(hoursFmt)
    ax.autoscale_view()
    ax.grid(True)
##    fig2.xlabel('Time')
##    fig2.ylabel('Kilowatt')
##    fig2.title('Detail usage for '+start.strftime('%m/%d/%Y'))

##    print timedata[:-1]
##    now = datetime.datetime.now() + datetime.timedelta(hours=-7)
    fig2.text(0.5, 0.95,'Detailed Energy Usage for %s (last updated %s)'% (date.strftime('%m/%d/%Y'), timedata[-1]) )






    fig2.savefig(filename)
    
    return filename
