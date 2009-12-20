#-*- coding:utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import *

DEBUG = getattr(settings, 'DEBUG', False)

urlpatterns = patterns('', 
	(r'^i18n/', include('django.conf.urls.i18n')), 
	(r'^accounts/', include('registration.urls')), 
	(r'^publisher/', include('publisher.urls')), 
)

# [debug]  
if DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)


