from django.conf.urls.defaults import *

urlpatterns = patterns('python_electric.apps.electric.views',

    (r'^$', 'bar_day_current'),
    (r'livedata/$','sparkline'),
    (r'livedata/data/$','livedata'),
    (r'bar/month/$', 'bar_month_current'), # bar year, month view
    (r'bar/(?P<year>\d{4})/(?P<month>\d{2})/$', 'bar_month'), # bar year, month view
    (r'bar/week/$', 'bar_week_current'),
    (r'bar/(?P<year>\d{4})/week/(?P<week>\d+)/$', 'bar_week'),
    (r'bar/day/$', 'bar_day_current'),
    (r'bar/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$', 'bar_day'), # bar year, month, day view
    (r'timeline/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$', 'timeline_sec'), # bar year, month, day view
    (r'bills/$','bills'),
    
)
