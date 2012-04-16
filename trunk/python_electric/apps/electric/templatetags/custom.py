from django import template
import datetime
from dateutil.relativedelta import relativedelta

register = template.Library()

@register.filter
def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)

@register.filter
def hour(value):
    if value.hour == 12:
        return value.strftime("%Ip")
    elif value.hour == 0:
        return value.strftime("%Ia")
    elif value.hour > 12:
        return value.hour - 12
    else:
        return value.hour

@register.filter
def previousday(value, arg):
    value = value - datetime.timedelta(days=1)
    arg = str(arg)
    return value.strftime(arg)

@register.filter
def nextday(value, arg):
    value = value + datetime.timedelta(days=1)
    now = datetime.datetime.now()
    
    if value > now:
        return 'day/'
    else:
        arg = str(arg)
        return value.strftime(arg)

@register.filter
def previousweek(value, arg):
    value = value - datetime.timedelta(weeks=1)
    arg = str(arg)
    return value.strftime(arg)

@register.filter
def nextweek(value, arg):
    value = value + datetime.timedelta(weeks=1)
    now = datetime.datetime.now()
    
    if value > now:
        return ''
    else:
        arg = str(arg)
        return value.strftime(arg)

@register.filter
def previousmonth(value, arg):
    value = value - relativedelta(months=1)
    arg = str(arg)
    return value.strftime(arg)

@register.filter
def nextmonth(value, arg):
    value = value + relativedelta(months=1)
    now = datetime.datetime.now()

    if value > now:
        return ''
    else:
        arg = str(arg)
        return value.strftime(arg)

@register.filter
def percent(value):
    """
        returns percent % and positive
    """
    return '%.0f' % abs(round(value * 100))

@register.filter
def istoday(value):
    "returns boolean TRUE if date is today"
    now = datetime.datetime.now()
    if type(value) is not type(now):
        return False
    if value.year == now.year and value.month == now.month and value.day == now.day:
        return True
    else:
        return False

@register.filter
def iscurrentweek(value):
    "returns boolean TRUE if date is this week"
    now = datetime.datetime.now()
    if value.year == now.year and int(value.strftime('%U')) == int(now.strftime('%U')):
        return True
    else:
        return False
    
@register.filter
def iscurrentmonth(value):
    "returns boolean TRUE if date is on this month"
    now = datetime.datetime.now()
    if value.year == now.year and value.month == now.month:
        return True
    else:
        return False

@register.filter
def absolute(value):
    'returns the abs() value'
    return abs(value)
