from django.conf import settings as _settings
import re

def menu(request):

    path = request.path.strip('/')
    path = path.split('/')

    m = [
        ['Home', '/', False],
        ['Electricity', '/electric/', False],
        ['Water', '/water/', False],
        ['Oil/Gas', '/fuel/', False],
        ['Settings', '/admin/', False],
    ]

    for item in m:
        if item[1].replace('/','') == str(path[0]):
            item[2] = True

    return {'menu_nav':m}

def menu_electric(request):

#    (r'^$', 'bar_day_current'),
#    (r'livedata/$','sparkline'),
#    (r'livedata/data/$','livedata'),
#    (r'bar/month/$', 'bar_month_current'), # bar year, month view
#    (r'bar/(?P<year>\d{4})/(?P<month>\d{2})/$', 'bar_month'), # bar year, month view
#    (r'bar/week/$', 'bar_week_current'),
#    (r'bar/(?P<year>\d{4})/week/(?P<week>\d+)/$', 'bar_week'),
#    (r'bar/day/$', 'bar_day_current'),
#    (r'bar/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$', 'bar_day'), # bar year, month, day view
#    (r'timeline/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$', 'timeline_sec'), # bar year, month, day view
#    (r'bills/$','bills'),

    m = [
        ['day', '/electric/bar/day/', False, [r'/electric/$',
                                              r'bar/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$',
                                              r'bar/day/$']],
        ['week', '/electric/bar/week/', False, [r'bar/week/$',
                                                r'bar/(?P<year>\d{4})/week/(?P<week>\d+)/$']],
        ['month', '/electric/bar/month/', False, [r'bar/month/$',
                                                  r'bar/(?P<year>\d{4})/(?P<month>\d{2})/$']],
        ['live data', '/electric/livedata/', False, [r'livedata/$']],
        ['bills', '/electric/bills/', False, [r'bills/$']],
    ]

    for item in m:
        for i in item[3]:
            if re.search(i, request.path):
                item[2] = True

    return {'menu_electric':m}

def settings(request):
    return {'settings': _settings}
