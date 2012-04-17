from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# electric...
	(r'^electric/', include('python_electric.apps.electric.urls')),

    # Uncomment the next line to enable the admin:
   (r'^admin/', include(admin.site.urls)),
   
)

# this is to allow django to serve static files during development, not for use during production
# https://docs.djangoproject.com/en/dev/howto/static-files/
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )