from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

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
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()