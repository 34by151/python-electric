from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.db import connection

import json

from python_electric.apps.electric.models import *
from charts import *
from settings import CHART, ELECTRICITY
import TED

gateway = TED.Gateway()

##def datetime_now():
##    now = datetime.datetime.now()# + datetime.timedelta(hours=-7)
##    return now

def getcurrentcost(date):
    history = utility_bill.objects.filter(DATE_START__lte=date)
    history = history.order_by('-DATE_END')
    
    if len(history) > 0:
        item = history[0]
        cost = item.COST/(item.POWER_END - item.POWER_START)
        return cost, item.DATE_END
    else:
        return Decimal(ELECTRICITY.RATE), None

def getdailybudget(date):
    budget_item = daily_budget.objects.filter(date__lte=date)
    budget_item = budget_item.order_by('-date')

    if len(budget_item) > 0:
        budget = [float(budget_item[0].night), float(budget_item[0].morning),
                float(budget_item[0].afternoon), float(budget_item[0].evening)]
        budgetdate = budget_item[0].date
    else:
        budget = CHART.BUDGET_DAY
        budgetdate = None

    return budget, budgetdate

def getweeklybudget(date):
    budget, budgetdate = getdailybudget(date)
    budget = [sum(budget)] * 7
    return budget, budgetdate



def sparkline(request):
    return render_to_response ('electric/sparkline.html', {'data' : None}, context_instance=RequestContext(request))


def timeline_sec(request, year, month, day):
    
    #date = datetime.datetime(int(year), int(month), int(day))
    start = datetime.datetime (int(year), int(month), int(day))
    #start = datetime.datetime (int(year), int(month), int(day), 21, 00, 00)
    end = datetime.datetime (int(year), int(month), int(day), 23, 59, 59)
    
    history = TED_history_second.objects.filter(DATE__gte=start)
    history = history.filter(DATE__lte=end)
    history = history.filter(FILTER__exact=0)
    history = history.order_by('-DATE')    
    
    return render_to_response ('electric/timeline.html', {'data' : history, 'date' : start}, context_instance=RequestContext(request))

def bar_day_current (request):
    now = datetime.datetime.now()
    return bar_day(request, now.year, now.month, now.day)


def bar_day(request, year, month, day):

    # date functions...
    now = datetime.datetime.now()

    year = int(year)
    month = int(month)
    day = int(day)

    # the start of the requested date
    start = datetime.datetime(year, month, day)

    # the end of the requested date
    end = start.replace(hour = 23, minute = 59)

    ###### DAILY HISTOGRAM ######
    
    # initialize objects
    data = []
    statistics = {}
    kwtotal = Decimal(0)
    cost, lastbill = getcurrentcost(start)

    # fill data object with empty power values as placeholders
    for hour in range (0, 24):
        date = start.replace(hour=hour)
        data.append({'POWER' : 0, 'DATE' : date})
    
    # if requesting data for today, get minute data for the current hour
    if year == now.year and month == now.month and day == now.day:
        
        hour_start = start.replace (hour=now.hour)
        hour_end = hour_start + datetime.timedelta(hours=1)
        
        # Django Development command...
        # hour_sum = TED_history_minute.objects.raw('SELECT sum(POWER) FROM TED_history_minute WHERE DATE >= %s', [hour_start])
        
        # Django 1.1 command...
        cursor = connection.cursor()
        cursor.execute("SELECT sum(POWER) FROM TED_history_minute WHERE DATE >= %s AND DATE < %s", [hour_start, hour_end])
        hour_sum = cursor.fetchone()[0]
        # end
    
        # add current hour to data object...
        if hour_sum:
            data[hour_start.hour] = {'POWER' : hour_sum/60, 'DATE' : hour_start}


        # Fill in previous hour as well, just in case TED data hasn't been updated yet...
        hour_start = start.replace (hour=now.hour)-datetime.timedelta(hours=1)
        if hour_start.day == now.day:
            hour_end = start.replace (hour=now.hour)
        
            # Django 1.1 command...
            cursor = connection.cursor()
            cursor.execute("SELECT sum(POWER) FROM TED_history_minute WHERE DATE >= %s AND DATE < %s", [hour_start, hour_end])
            hour_sum = cursor.fetchone()[0]
            # end
        
            # add last hour to data object...
            if hour_sum:
                data[hour_start.hour] = {'POWER' : hour_sum/60, 'DATE' : hour_start}
    
    # get hour history for the requested day...
    history = TED_history_hour.objects.filter(DATE__gte=start)
    history = history.filter(DATE__lte=end)
    history = history.order_by('DATE')
    
    for item in list(history):
        # insert history in data...
        hour = item.DATE.hour
        data[hour] = {'POWER' : item.POWER, 'DATE' : item.DATE}
        
    # calculate totals for the day
    for item in data:
        kwtotal += item['POWER']

    # get the budget for today
    budget, budgetdate = getdailybudget(date = start)

    current = [0.0, 0.0, 0.0, 0.0]

    for item in list(data):
        # insert history in data...
        date = item['DATE']
        hour = date.hour
        
        # group power for budget chart...
        if hour < 6:
            # add to night
            current[0] += float(item['POWER'])
        elif hour < 12:
            # add to morning
            current[1] += float(item['POWER'])
        elif hour < 18:
            # add to afternoon
            current[2] += float(item['POWER'])
        elif hour < 24:
            # add to evening
            current[3] += float(item['POWER'])
   
    hourchart = CreateDayHourChart (start, data, cost=cost)
    budgetchart, budgetpercent = CreateDayBudgetChart (end, current, budget)

    ############################## AVERAGES   

    history = average_day.objects.filter(DATE__gte=start-datetime.timedelta(days=7*20+1))
    history = history.filter(DATE__lte=start-datetime.timedelta(days=1))
    history = history.order_by('DATE')

    averages = []
    
    ################### break down the list and use as seperate arguments... could be used on other charts
    for item in list(history):
        averages.append([item.DATE, item.POWER7, item.POWER14, item.POWER21, item.POWER28])

    averagechart = CreateAverageChart (averages, cost=cost)

    #############################################
    #history = TED_history_second.objects.filter(DATE__gte=start)
    #history = history.filter(DATE__lte=end)
    #history = history.order_by('-DATE')    
    #target = 0.0
    #data_second = []
    #for item in history:
    #    if abs(float(item.POWER) - target) > 0.001:
    #        target = float(item.POWER)
    #        data_second.append(item.POWER)    
    #detailchart = CreateDayDetailChart (data_second)
    ###############################################

    
    # Django 1.1 command...
    cursor = connection.cursor()
    
    items = [   ['average7', 'SELECT POWER7 FROM electric_average_day WHERE DATE = %s', [start-datetime.timedelta(days=1)]],
                ['average14', 'SELECT POWER14 FROM electric_average_day WHERE DATE = %s', [start-datetime.timedelta(days=1)]],
                ['average28', 'SELECT POWER28 FROM electric_average_day WHERE DATE = %s', [start-datetime.timedelta(days=1)]],
                ['average7_prime', 'SELECT POWER7 FROM electric_average_day WHERE DATE = %s', [start-datetime.timedelta(days=2)]],
                ['average14_prime', 'SELECT POWER14 FROM electric_average_day WHERE DATE = %s', [start-datetime.timedelta(days=2)]],
                ['average28_prime', 'SELECT POWER28 FROM electric_average_day WHERE DATE = %s', [start-datetime.timedelta(days=2)]],
                ['lastupdate', 'select MAX(date) from TED_history_minute where MTU = %s', [0]],
#                ['<td>Max</td><td><strong>%s</strong> kW @ (time)</td>', 'SELECT max(POWER) FROM TED_history_second WHERE DATE >= %s AND DATE < %s', [start, end]], 
#                ['<td>Min</td><td><strong>%s</strong> kW @ (time)</td>', 'SELECT min(POWER) FROM TED_history_second WHERE DATE >= %s AND DATE < %s', [start, end]],
                ]

    
    for key, query, daterange in items:
        cursor.execute(query, daterange)
        x = cursor.fetchone()
        
        if x:
            if len(x) > 0:
                if x[0] <> None:
                    statistics[key] = x[0]
    
    statistics['kwtotal'] = kwtotal
    statistics['kwtotalcost'] = kwtotal*cost
    statistics['kwyearcost'] = kwtotal*cost*Decimal('365.242199')
    statistics['kwbudget'] = kwtotal * Decimal(str(budgetpercent)) #kwtotal-Decimal(str(sum(budget)))
    statistics['kwbudgetcost'] = (kwtotal-Decimal(str(sum(budget))))*cost
    statistics['budgetdate'] = budgetdate
    statistics['kwcost'] = cost
    statistics['lastbill'] = lastbill
    statistics['budgetpercent'] = budgetpercent
    statistics['average7_delta'] = (statistics['average7']-statistics['average7_prime'])/statistics['average7_prime']
    statistics['average14_delta'] = (statistics['average14']-statistics['average14_prime'])/statistics['average14_prime']
    statistics['average28_delta'] = (statistics['average28']-statistics['average28_prime'])/statistics['average28_prime']


    return render_to_response ('electric/bar_day.html',
            {'hourchart': hourchart,
             'date' : start,
             'budgetchart': budgetchart,
             'averagechart': averagechart,
             'statistics' : statistics},
            context_instance=RequestContext(request))

def bar_week_current (request):
    now = datetime.datetime.now()
    week = now.strftime('%U')
    return bar_week(request, now.year, week)


def bar_week(request, year, week):

    now = datetime.datetime.now()
    
    year = int(year)
    week = int(week)
    
    year_start = datetime.datetime(year, 1, 1)
    week0 = year_start - datetime.timedelta(days=year_start.isoweekday())
    weekrequest = week0 + datetime.timedelta(weeks=week)
    start = weekrequest - datetime.timedelta(weeks=1)
    end = weekrequest + datetime.timedelta(weeks=1)
    start_scatter = weekrequest
    end_scatter = end


    data = []
    kwtotal = Decimal(0)
    kwtotal_lastweek = Decimal(0)
    current = [0.0]*7*2
    budget, budgetdate = getweeklybudget(weekrequest)
    #budget = CHART.BUDGET_WEEK
    cost, lastbill = getcurrentcost(weekrequest)


    for day in range (0, 7*2):
        date = start + datetime.timedelta(days=day)
        data.append({'POWER' : 0, 'DATE' : date})


    if year == now.year and week == int(now.strftime('%U')):

        dayofweek = int(now.strftime('%w')) + 7

        # Get the SUM for the current week...
        day_start = datetime.datetime(now.year, now.month, now.day)
        # Django Development command...
        #day_sum = TED_history_minute.objects.raw('SELECT sum(POWER) FROM TED_history_minute WHERE DATE >= %s', [day_start])

        # Django 1.1 command...
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("SELECT sum(POWER) FROM TED_history_minute WHERE DATE >= %s", [day_start])
        day_sum = cursor.fetchone()[0]
        # end

        if day_sum:
            data[dayofweek] = {'POWER' : day_sum/60, 'DATE' : day_start}
            ##colors[dayofweek] = '70d070'
            current[dayofweek] = float(day_sum)/60
            kwtotal = Decimal(day_sum)/60

        # get the last 7 days for the scatter
        # start_scatter = now - datetime.timedelta(weeks=1)
        # start_scatter = datetime.datetime(year=start_scatter.year, month=start_scatter.month, day=start_scatter.day,
        #                                   hour=0, minute=0, second=0)

    history = TED_history_day.objects.filter(DATE__gte=start)
    history = history.filter(DATE__lt=end)
    history = history.order_by('DATE')

    for item in list(history):
        diff = item.DATE - start
        #print "diff: %s, start: %s, item.DATE: %s" % (diff.days, start, item.DATE)
        data[diff.days] = {'POWER' : item.POWER, 'DATE' : item.DATE}
        current[diff.days] = float(item.POWER)
        if diff.days > 6:
            # add the total for the requested week...
            kwtotal += item.POWER
        else:
            kwtotal_lastweek += item.POWER

    current[0:7] = []
    
    weekchart = CreateWeekDayChart (data, cost=cost)
    budgetchart = CreateWeeklyBudgetChart (year, week, current, budget)
    
    data = []
    max = 0
    
    # create empty matrix
    for hour in range (0, 7*24):
        date = weekrequest + datetime.timedelta(hours=hour)
        data.append({'POWER' : 0, 'DATE' : date})        
        
    if year == now.year and week == int(now.strftime('%U')):
       
        # Get the SUM for the current week...
        hour_start = datetime.datetime(now.year, now.month, now.day, now.hour)
        hour_end = hour_start + datetime.timedelta(hours=1)
        # Django Development command...
        # hour_sum = TED_history_minute.objects.raw('SELECT sum(POWER) FROM TED_history_minute WHERE DATE >= %s', [hour_start])
    
        # Django 1.1 command...
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("SELECT sum(POWER) FROM TED_history_minute WHERE DATE >= %s AND DATE < %s", [hour_start, hour_end])
        hour_sum = cursor.fetchone()[0]
        # end


        if hour_sum:
            dayofweek = int(now.strftime('%w'))
            hour_sum = hour_sum / 60
            data[24 * dayofweek + now.hour] = {'POWER' : hour_sum, 'DATE' : hour_start}
            max = hour_sum

        
    history = TED_history_hour.objects.filter(DATE__gte=weekrequest)
    history = history.filter(DATE__lte=end)
    history = history.order_by('DATE')
    
    for item in list(history):
        hour = int(item.DATE.strftime("%H"))
        weekday = int(item.DATE.strftime("%w"))
        i = 24 * weekday + hour
        data[i] = {'POWER' : item.POWER, 'DATE' : item.DATE }
        if max < item.POWER:
            max = item.POWER

    scatter = CreateWeekScatterChart(data)

    statistics = {}

    from django.db import connection
    cursor = connection.cursor()

    items = [
        ['lastupdate', 'select MAX(date) from TED_history_minute where MTU = %s', [0]],
        #['lastweek', 'select SUM(power) from TED_history_hour where MTU = %s', [0]],

                ]


    for key, query, daterange in items:
        #print "10 (%s)= %s" % (key, time.time()-timerstart)
        cursor.execute(query, daterange)
        x = cursor.fetchone()

        if x:
            if len(x) > 0:
                if x[0]:
                    statistics[key] = x[0]

    #print "11 = %s" % (time.time()-timerstart)

    statistics['kwtotal'] = kwtotal
    statistics['kwtotalcost'] = kwtotal*cost
    statistics['kwyearcost'] = kwtotal*cost*Decimal('52.177457')
    statistics['kwbudget'] = kwtotal-Decimal(str(sum(budget)))
    statistics['kwbudgetcost'] = (kwtotal-Decimal(str(sum(budget))))*cost
    statistics['budgetdate'] = budgetdate
    statistics['kwcost'] = cost
    statistics['lastbill'] = lastbill
    statistics['lastweek'] = kwtotal - kwtotal_lastweek
    
    return render_to_response ('electric/bar_week.html',
            {'weekchart':weekchart,
             'date' : weekrequest,
             'budgetchart' : budgetchart,
             'scatterchart' : scatter,
             'statistics' : statistics},
                               context_instance=RequestContext(request))

def bar_month_current (request):
    now = datetime.datetime.now()
    return bar_month(request, now.year, now.month)

def bar_month(request, year, month):

    now = datetime.datetime.now()
    
    year = int(year)
    month = int(month)
    
    start = datetime.datetime(year, month, 1)
        
    if start.month == 12:
        end = start.replace(day=31)
    else:
        end = start.replace(month=start.month+1) - datetime.timedelta(days=1)
    
    numbofdays = end - start
    data = []
    cost, lastbill = getcurrentcost(date=start)
    
    for day in range (0, numbofdays.days+1):
        date = start.replace(day=day+1)
        data.append({'POWER' : 0, 'DATE' : date})
    
    if year == now.year and month == now.month:
        ## get current day's minute data...    
        day_start = datetime.datetime(now.year, now.month, now.day)
        # Django Development command...
        # hour_sum = TED_history_minute.objects.raw('SELECT sum(POWER) FROM TED_history_minute WHERE DATE >= %s', [hour_start])
        
        # Django 1.1 command...
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("SELECT sum(POWER) FROM TED_history_minute WHERE DATE >= %s", [day_start])
        day_sum = cursor.fetchone()[0]
        # end
    
        if day_sum:
            data[now.day-1] = {'POWER' : day_sum/60, 'DATE' : day_start}
    
    
    history = TED_history_day.objects.filter(DATE__gte=start)
    history = history.filter(DATE__lte=end)
    history = history.order_by('DATE')
    
    for item in list(history):
        day = item.DATE.day
        data[day-1] = {'POWER' : item.POWER, 'DATE' : item.DATE}

   
    monthchart = CreateMonthDayChart (data, cost=cost)

    # Previous Months Data... 
    numberofyears = 2
    numberofmonths = (12*numberofyears)
    data = [None]*numberofmonths
    startyear = start.replace(year=start.year-numberofyears)
    if startyear.month == 12:
        startyear = datetime.datetime (year=startyear.year+1, month=1, day=1)
    else:
        startyear = startyear.replace(month=startyear.month+1)
    date = startyear
    endyear = datetime.datetime (year=end.year, month=end.month, day=end.day, hour=23, minute=59, second=59)
    for i in range (0, numberofmonths):
        data[i] = {'POWER' : 0, 'DATE' : date, 'DAYS' : 0, 'AVERAGE' : 0}
        if date.month == 12:
            date = datetime.datetime (year=date.year+1, month=1, day=1)
        else:
            date = date.replace(month=date.month+1)
    days = [0] * numberofmonths
    history = TED_history_day.objects.filter(DATE__gte=startyear)
    history = history.filter(DATE__lt=endyear)
    history = history.order_by('DATE')
    for item in list(history): 
        date = item.DATE
        power = item.POWER
        diff_month = date.month - startyear.month
        diff_year = date.year - startyear.year
        if diff_year >= 0: 
            diff = 12 * diff_year + diff_month
        power += data[diff]['POWER']
        days[diff] += 1
        average = power/days[diff]
        data[diff]={'POWER' : power, 'DATE' : datetime.datetime(date.year, date.month, 1), 'DAYS' : days[diff], 'AVERAGE' : average}
##    for i in range(0,len(data)):
##        print i, data[i]
    yearchart = CreateYearMonthChart (data)
    
    return render_to_response ('electric/bar_month.html', {'monthchart': monthchart, 'yearchart': yearchart, 'date' : start,}, context_instance=RequestContext(request))

def livedata(request):
    # Get Live Data from TED...
    gateway.GetLiveData ()
    
    # Get Values from TED...
    currentdate = gateway.GatewayTime()
    power = gateway.PowerNow(0)
    voltage = gateway.Voltage(0,'VoltageNow')
    kva = gateway.Power(0,'KVA')
    
    data = json.dumps({ 'time' : currentdate.strftime('%I:%M:%S'),
                        'power' : power,
                        'voltage' : voltage,
                        'kva' : kva})


    if request.is_ajax():
        message = data
    # If you want to prevent non XHR calls
    else:
        message = data  ## for testing only
        #return HttpResponse(status=400)
    
    return HttpResponse(message)

    
def bills(request):
    history = utility_bill.objects.all()
    history = history.order_by('DATE_END')

    data = []
    start = 0
    end = 0

    for item in list(history):
        consumption = item.POWER_END - item.POWER_START
        costperwatt = item.COST/(item.POWER_END - item.POWER_START)
        diff = item.DATE_END - item.DATE_START
        days = diff.days
        avg_watt_per_day = (item.POWER_END - item.POWER_START)/days
        avg_cost_per_day = item.COST/days
        # insert history in data...
        data.append ({'DATE_START' : item.DATE_START,
                      'DATE' : item.DATE_END,
                      'POWER_START' : item.POWER_START,
                      'POWER_END' : item.POWER_END,
                      'POWER' : consumption,
                      'COST' : item.COST,
                      'COSTWATT' : costperwatt, 
                      'DAYS' : days,
                      'AVERAGE' : avg_watt_per_day,
                      'COSTDAY' : avg_cost_per_day, })


    yearchart = CreateYearMonthChart (data)


    return render_to_response ('electric/bills.html', {'bills': data, 'yearchart':yearchart}, context_instance=RequestContext(request))
