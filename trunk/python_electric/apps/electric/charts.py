import datetime, string
from GChartWrapper import *
from settings import CHART, ELECTRICITY
from decimal import *

import os
os.environ['HOME'] = CHART.PATH

# do this before importing pylab or pyplot
import matplotlib
matplotlib.use('Agg')
import pylab as plt
from matplotlib.dates import HourLocator, DateFormatter


chartcolor = '#afafaf'
textcolor = '#6e6e6e'

width = CHART.WIDTH

def CreateDayHourChart (start, data, cost=ELECTRICITY.RATE):
    now = datetime.datetime.now()
    x = []
    d = []
    mx = Decimal(CHART.Y_MAX)
    y_max = 4095
    x_label = ['12a', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                '12p', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

    color = []

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
            color.append (CHART.COLOR_CURRENT_3)
        else:
            color.append (CHART.COLOR_CURRENT_1)
    
    bottom = 0
    top = int(float(mx)+float(0.999999999999))
    step = 1
    
    scale = y_max/(top-bottom)
    
    for i in range (0, len(x)):
        x[i] = x[i] * scale
        if x[i] > y_max:
            x[i] = y_max
    
   
    G = VerticalBarStack([x], encoding='extended')
    G.color('|'.join(color))

    G.size(width, 150)
    G.margin(0, 0, 10, 10)
    
    G.axes('xyr')

    G.axes.range(1, bottom, top*cost, cost)
    G.axes.range(2, bottom, top, step)
    
    G.axes.label(0, '|'.join(x_label))
    y_label_cost = ['%.2f' % (i*cost) for i in range(bottom, top+1, step)]
    G.axes.label(1, '|'.join(y_label_cost))
    
    # bar thickness and spacing
    G.bar('r', 0.1, 0.1)
    
    G.grid(0, 99.9/(top-bottom), 1, 0)
    
    # electricity in kW label
    G.marker ('@telectricity in kW h', '666666', 0, '1:1', 10)
    G.marker ('@telectricity in $', '666666', 0, '0:1', 10)
    
    return str(G)


def CreateWeekDayChart (data, cost=ELECTRICITY.RATE):
    
    now = datetime.datetime.now()
    x = []
    d = []
    mx = Decimal(CHART.Y_MAX)
    y_max = 4095
    x_label = []
    color = []

    for item in data:
        power = item['POWER']
        date = item['DATE']
        
        x.append(float(power))
        x_label.append(date.strftime('%a-')+str(date.day))
        
        if date.year == now.year and date.month == now.month and date.day == now.day:
            color.append (CHART.COLOR_CURRENT_3)
        elif date.strftime('%U') == now.strftime('%U'):
            if date.strftime('%w') in ['0','6']:
                color.append (CHART.COLOR_CURRENT_2)
            else:
                color.append (CHART.COLOR_CURRENT_1)
        elif date.strftime('%w') in ['0','6']:
            color.append (CHART.COLOR_HISTORICAL_2)
        else:
            color.append (CHART.COLOR_HISTORICAL_1)
     
        if power == 0:
            pass
        else:
            if power > mx:
                mx = power

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

    scale = y_max/(top-bottom)

    for i in range (0, len(x)):
        x[i] = x[i] * scale
        if x[i] > y_max:
            print "Error: x[%s]=%s is greater than %s.  Scale of %s is wrong!" % (i, x[i], y_max, scale)
    
   
    G = VerticalBarStack([x], encoding='extended')

    G.color('|'.join(color))

    G.size(width,150)
    G.margin(0,0,10,10)
    
    G.axes('xyr')

    G.axes.range(1, bottom,top*cost,step*cost)
    G.axes.range(2, bottom,top,step)

    G.axes.label(0, '|'.join(x_label))
    y_label_cost = ['%.2f' % (i*cost) for i in range(bottom, top+1, step)]
    G.axes.label(1, '|'.join(y_label_cost))
    # bar thickness and spacing
    G.bar('r', 0.1, 0.1)
    
    G.grid(0, 99.9/(top-bottom)*step, 1, 0)
    
    # electricity in kW label
    G.marker ('@telectricity in kW h', '666666', 0, '1:1', 10)
    G.marker ('@telectricity in $', '666666', 0, '0:1', 10)
    
    return str(G)

def CreateWeekScatterChart (data):
    now = datetime.datetime.now()
    x = []
    #d = []
    mx = 0
    x_label = ['','12a','1','2','3','4','5','6','7','8','9','10','11','12p','1','2','3','4','5','6','7','8','9','10','11','']
    y_label = ['','Sun','Mon','Tue','Wed','Thr','Fri','Sat','']
    color = []
    dotsize = int(25.0*width/600)
    chd_1 = []
    for i in range (0,24):
        chd_1.append(str(i))
    chd_1 *= 8
    chd_2 = []
    for i in range (0,8):
        for k in range (0,24):
            chd_2.append(str(i))
    chd_3 = ['0.0']*24*8 # *8 for an extra row of zeros

    for item in data:
        power = item['POWER']
        date = item['DATE']
        x.append(float(power))
        if date.year == now.year and date.month == now.month and date.day == now.day:
            if date.hour == now.hour:
                color.append (CHART.COLOR_CURRENT_3)
            else:
                color.append (CHART.COLOR_CURRENT_1)
        else:
            color.append (CHART.COLOR_HISTORICAL_1)
        if power > mx:
            mx = power
        
    if not mx:
         scale = 0
    else:
         scale = float(dotsize/mx)

    for i in range (0, len(x)):
        chd_3[i] = str(int(round(x[i] * scale, 0)))

    G = Scatter([chd_1, chd_2, chd_3], encoding='text')

    G.size(width,width/3)

    G.scale (-1,24,-1,7,0,int(dotsize*.75))
    G.axes('xy')
    G.marker('o',CHART.COLOR_HISTORICAL_2,1,-1,dotsize)
    G.axes.label(0, '|'.join(x_label))
    G.axes.label(1, '|'.join(y_label))
    
    # electricity in kW label
    G.marker ('@tmax ' + str(round(mx,1)) + 'kW h', '666666', 0, '1:1', 10,1)

    return str(G)    


def CreateMonthDayChart (data, cost=ELECTRICITY.RATE):
    
    now = datetime.datetime.now()
    x = []
    mx = Decimal(CHART.Y_MAX)
    y_max = 4095
    x_label = []
    color = []

    for item in data:
        power = item['POWER']
        date = item['DATE']
        
        x.append(float(power))
        x_label.append(str(date.day))
        
        if date.year == now.year and date.month == now.month and date.day == now.day:
            color.append (CHART.COLOR_CURRENT_3)
        elif date.strftime('%w') in ['0','6']:
            color.append (CHART.COLOR_CURRENT_2)
        else:
            color.append (CHART.COLOR_CURRENT_1)
     
        if not power:
            pass
        else:
            if power > mx:
                mx = power
        
    bottom = 0
    top = (int(mx/10)+1)*10
    step = (int(mx/10)+1)*2
    
    scale = float(y_max/(top-bottom))
    
    for i in range (0, len(x)):
        x[i] = x[i] * scale
        if x[i] > y_max:
            print "Error: x[%s]=%s is greater than %s.  Scale of %s is wrong!" % (i, x[i], y_max, scale)
    
   
    G = VerticalBarStack([x], encoding='extended')

    G.color('|'.join(color))

    G.size(width,150)
    G.margin(0,0,10,10)
    
    G.axes('xyr') 

    G.axes.range(1, round(bottom*cost,2), round(top*cost,2), step*cost)
#    G.axes.range(1, bottom,top,step)
    G.axes.range(2, bottom, top, step)
    
    G.axes.label(0, '|'.join(x_label))
    y_label_cost = ['%.2f' % (i*cost) for i in range(bottom, top+1, step)]
    G.axes.label(1, '|'.join(y_label_cost))
    
    # bar thickness and spacing
    G.bar('r', 0.1, 0.1)
    
    G.grid(0, 99.9/(top-bottom)*step, 1, 0)
        
    # electricity in kW label
    G.marker ('@telectricity in kW h', '666666', 0, '1:1', 10)
    G.marker ('@telectricity in $', '666666', 0, '0:1', 10)
    return str(G)

def CreateYearMonthChart (data):
    now = datetime.datetime.now()
    
    x = []
    x2 = []
    d = []
    mx_1 = Decimal(CHART.Y_MAX)
    mx_2 = Decimal(CHART.Y_MAX)
    mn_2 = Decimal(10000000)
    
    y_max = 4095.0
    x_label = []
    x2_label = []
    color = []

    #print "mx_1: %s (%s)" % (mx_1, type(mx_1))
            
    for item in data:
        power = item['POWER']
        date = item['DATE']
        average = item['AVERAGE']
        
        x.append(float(power))
        x2.append(float(average))
        x_label.append(date.strftime('%b'))
        if date.strftime('%Y') in x2_label:
            x2_label.append('')
        else:
            x2_label.append(date.strftime('%Y'))
        
        if date.year == now.year and date.month == now.month:
            color.append (CHART.COLOR_CURRENT_3)
        else:
            color.append (CHART.COLOR_HISTORICAL_1)
     
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
    
    bottom_2 = (int(mn_2/10))*10
    top_2 = (int(mx_2/10)+1)*10
    scale_2 = y_max/(top_2-bottom_2)
    step_2 = (int((top_2-bottom_2)/10))*2

    grid=100.0/(top_1-bottom_1)*step_1

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
    
    G.axes('xyrx') 

    G.axes.range(1, bottom_1,top_1,step_1)
    G.axes.range(2, bottom_2,top_2,step_2)
##    G.axes.range(1, bottom_1,top_1,(top_1-bottom_1)/4)
##    G.axes.range(2, bottom_2,top_2,(top_2-bottom_2)/4)
    G.axes.label(0, '|'.join(x_label))
    G.axes.label(3, '|'.join(x2_label))
    
    # bar thickness and spacing
    G.bar('r', 0.1, 0.1)
    
    G.grid(0, grid, 1, 0)
    
    # electricity in kW label
    G.marker ('@taverage in kW h/day', '666666', 0, '1:1', 10)
    G.marker ('@ttotal in kW h', '666666', 0, '0:1', 10)

    return str(G)
    
    
def CreateDayBudgetChart (date, current, budget):
    
    now = datetime.datetime.now()

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
    b_label = b_max
    
    b_length = (width-100)*b_max # needs to be offset a little

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
        c_sq501_label = 'n'
    else:
        c_sq501_label = ''
        
    if c_sq502-c_sq501 > 0.06:
        c_sq502_label = 'morning'
    elif c_sq502-c_sq501 > 0.03:
        c_sq502_label = 'm'
    else:
        c_sq502_label = ''

    if c_sq503-c_sq502 > 0.08:
        c_sq503_label = 'afternoon'
    elif c_sq503-c_sq502 > 0.04:
        c_sq503_label = 'a'
    else:
        c_sq503_label = ''

    if c_label-c_sq503 > 0.05:
        c_sq504_label = 'evening'
    elif c_label-c_sq503 > 0.03:
        c_sq504_label = 'e'
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
    if b_sq501 > 0.04:
        b_sq501_label = 'night'
    elif b_sq501 > 0.03:
        b_sq501_label = 'n'
    else:
        b_sq501_label = ''

    if b_sq502-b_sq501 > 0.06:
        b_sq502_label = 'morning'
    elif c_sq502-c_sq501 > 0.03:
        b_sq502_label = 'm'
    else:
        b_sq502_label = ''

    if b_sq503-b_sq502 > 0.08:
        b_sq503_label = 'afternoon'
    elif b_sq503-b_sq502 > 0.04:
        b_sq503_label = 'a'
    else:
        b_sq503_label = ''

    if b_label-b_sq503 > 0.05:
        b_sq504_label = 'evening'
    elif b_label-b_sq503 > 0.03:
        b_sq504_label = 'e'
    else:
        b_sq504_label = ''

    if date.year == now.year and date.month == now.month and date.day == now.day:
        text = r"@ysq'i\=" + str(b_length) + r"'=13'scl'\c0c0c0'c"
        G.marker (text, '', 0, '0.5:0', 0, -1) # controls length of historical light gray area
    G.marker (r"@y%s'h\=10'f\fff'c\h-0-10'a\<=67''scl'" % b_sq501_label, '', 0, '0.5:' + str(b_night), 0) # adds 'night'
    G.marker (r"@ysq50'i\=1'=13'scl'\fff'c", '', 0, '0.5:' + str(b_sq501), 0) # adds night divider
    G.marker (r"@y%s'h\=10'f\fff'c\h-0-10'a\<=220''scl'" % b_sq502_label, '', 0, '0.5:' + str(b_morning), 0) # adds 'morning'
    G.marker (r"@ysq50'i\=1'=13'scl'\fff'c", '', 0, '0.5:' + str(b_sq502),0) # adds morning divider
    G.marker (r"@y%s'h\=10'f\fff'c\h-0-10'a\<=397''scl'" % b_sq503_label, '', 0, '0.5:' + str(b_afternoon), 0) # adds 'afternoon'
    G.marker (r"@ysq50'i\=1'=13'scl'\fff'c", '', 0, '0.5:' + str(b_sq503), 0) # controls historical afternoon divider
    G.marker (r"@y%s'h\=10'f\fff'c\h-0-10'a\<=181''scl'" % b_sq504_label, '', 0, '0.5:' + str(b_evening), 0) # adds 'evening'
    G.marker (r"@yl'h\=18'f\666666'c\l-0-13'a", '', 0, '0.5:' + str(b_label), 0) # adds emphasis marker on historical
    text = r"@y" + str(round(historical_total,1)) + r" kWh expected'h\=10'f\666666'c\-6-10'a"
    G.marker (text, '', 0, '0.5:' + str(b_label), 0)    

    return [str(G), percentage]
    



def CreateWeeklyBudgetChart (year, week, current, budget):
     
    now = datetime.datetime.now()

    year_start = datetime.datetime(year, 1, 1)
    week0 = year_start - datetime.timedelta(days=year_start.isoweekday())
    start = week0 + datetime.timedelta(weeks=week)
    
    if year == now.year and week == int(now.strftime('%U')):
        end = now
    else:
        end = start + datetime.timedelta(weeks=1) - datetime.timedelta(seconds=1)

    current_sum = 0.0
    for i in current:
        current_sum += i

    historical_total = 0.0
    for i in budget:
        historical_total += i

    kw_max = max(current_sum, historical_total)

    diff = end - start
    #i = diff.days + diff.seconds/float(60*60*24)

    historical_sum = 0.0

    for i in range(0,diff.days):
        historical_sum += budget[i]

    if diff.days < 7:
        historical_sum += budget[diff.days]*diff.seconds/float(60*60*24)

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
    c_label = current_sum/historical_total
    if c_label > 1:
        c_label = 1.0
    
    b_max =  historical_total/float(kw_max)
    b_label = b_max
    b_length = (width-112)*b_max

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

    # Set budget chart paramaters

    # cht=bhs
    # chd=e:ySAA,AA1Z
    bar_current = round(current_sum/kw_max * 100, 3)
    bar_budget = round(historical_sum/kw_max * 100, 3)
    G = HorizontalBarStack([[bar_current],[0,bar_budget]], encoding='text')

    # chs=425x34
    G.size(width,34)

    # chco=70d070,666666
    G.color(color, '666666')
    
    # chbh=13,1,1
    G.bar(13,1,1)
    
    # chxt=x,y,r
    G.axes('xyr')
    
    # chxl=2:
    #     210+kW%C2%B7h+expected
    #     160+kW%C2%B7h+used
    G.axes.label(2, 'total kilo Wh expected', '')

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

    G.marker ("@yS\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[0]), 0)
    if c_sq[1]-c_sq[0] > min_space:
        G.marker ("@yM\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[1]), 0)
    if c_sq[2]-c_sq[1] > min_space:
        G.marker ("@yT\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[2]), 0)
    if c_sq[3]-c_sq[2] > min_space:
        G.marker ("@yW\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[3]), 0)
    if c_sq[4]-c_sq[3] > min_space:
        G.marker ("@yT\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[4]), 0)
    if c_sq[5]-c_sq[4] > min_space:
        G.marker ("@yF\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[5]), 0)
    if c_sq[6]-c_sq[5] > min_space:
        G.marker ("@yS\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0:' + str(c_l[6]), 0)

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
    G.marker ("@yS\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[0]), 0)
    G.marker ("@yM\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[1]), 0)
    G.marker ("@yT\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[2]), 0)
    G.marker ("@yW\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[3]), 0)
    G.marker ("@yT\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[4]), 0)
    G.marker ("@yF\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[5]), 0)
    G.marker ("@yS\'h\\=9\'f\\fff\'c\\h-0-10\'a", '', 0, '0.5:' + str(b_l[6]), 0)
    
    # historical light gray area...
    # chm=@ysq'i\=999'=13'scl'\c0c0c0'c,,0,0.5:0,0,-1
    if year == now.year and week == int(now.strftime('%U')):
        G.marker (r"@ysq'i\=" + str(b_length) + r"'=13'scl'\c0c0c0'c", '', 0, '0.5:0', 0, -1) # controls length of historical light gray area
    
    
    #    @yl'h\=18'f\666666'c\l-0-13'a,,0,0.5:1,0
    G.marker (r"@yl'h\=18'f\666666'c\l-0-13'a", '', 0, '0.5:' + str(round(b_label,precision)), 0) # adds emphasis marker on historical
    
    # historical bar label for kwh used
    #     @y210+kW%C2%B7h+expected'h\=10'f\666666'c\-6-10'a,,0,0.5:1,0
    text = r"@y" + str(int(historical_total)) + r" kWh budget'h\=10'f\666666'c\-6-10'a"
    G.marker (text, '', 0, '0.5:' + str(round(b_label, precision)), 0)

    return G.url, percentage

def CreateAverageChart (data, cost=ELECTRICITY.RATE):
    
    mx = 0
    mn = 1000
    count = 0
    y_max = 4095
    #y_max = 100
    
    x_label = []
    y_label_cost = []

    now = datetime.datetime.now()
    
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
    G.color(CHART.COLOR_7, CHART.COLOR_28)
    G.legend('7 day','28 day')
    G.legend_pos('b')

    G.size(width,300)
    G.margin(0,0,10,10)

    dayofweek = int(d_start.strftime('%w'))
    x_stepsize = 99.9/(count-1)*7
    y_label_step = int(round((top-bottom)/10.0, ndigits=0))
    y_stepsize = 99.9/(top-bottom)*y_label_step
    x_offset = x_stepsize - dayofweek/7.0*x_stepsize
    
    G.axes('xyr') 
    G.axes.range(1, cost*bottom,cost*top,cost*y_label_step)
    G.axes.range(2, bottom,top,y_label_step)

    for i in range(bottom, top+1, y_label_step):
        y_label_cost.append('%.2f' % (i*cost))

    G.axes.label(1, '|'.join(y_label_cost))
    
    G.axes.label(0, '|'.join(x_label))

    G.grid(x_stepsize, y_stepsize, 1, 0, x_offset, 0)
    
    G.marker ('@telectricity in kW h', '666666', 0, '1:1', 10)
    G.marker ('@telectricity in $', '666666', 0, '0:1', 10)

    return str(G)

    
def CreateDayDetailChart (date, timedata, kwdata):

    inches = width/100.0
    matplotlib.rcParams['figure.figsize'] = '%s, 2' % inches
    matplotlib.rcParams['font.size'] = 8.5 # 12.0
    matplotlib.rcParams['font.family'] = 'arial' # sans-serif
    matplotlib.rcParams['text.color'] = 'orange'#textcolor # black
    matplotlib.rcParams['axes.edgecolor'] = chartcolor # axes edge color (black)
    matplotlib.rcParams['xtick.color'] = textcolor#'red'#chartcolor
    matplotlib.rcParams['ytick.color'] = textcolor#'yellow'#chartcolor
    matplotlib.rcParams['grid.color'] = chartcolor
    matplotlib.rcParams['lines.color'] = CHART.COLOR_CURRENT_3
    matplotlib.rcParams['lines.linewidth'] = 0.6

    #matplotlib.font_manager.FontProperties(family=None, style=None, variant=None, weight=None, stretch=None, size=None, fname=None, _init=None)
    #matplotlib.font_manager.FontProperties(stretch='expanded')
    
    hours = HourLocator() # Every Hour
    
    # figure 1 small
    
    filename = os.path.join(CHART.PATH, date.strftime('%Y%m%d-small.png'))
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
    filename = os.path.join(CHART.PATH, date.strftime('%Y%m%d.png'))
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
