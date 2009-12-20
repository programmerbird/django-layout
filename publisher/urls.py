#-*- coding:utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('publisher.views',
	(r'^layout/edit/(?P<layout_slug>[^\/]+)/$', 'edit_layout'),
	(r'^layout/remove/(?P<layout_id>\d+)/$', 'remove_layout'),
	(r'^layout/new/$', 'new_layout'),
	(r'^layout/$', 'layouts'),

	(r'^flatpage/edit/(?P<flatpage_id>\d+)/$', 'edit_flatpage'),
	(r'^flatpage/remove/(?P<flatpage_id>\d+)/$', 'remove_flatpage'),
	(r'^flatpage/new/$', 'new_flatpage'),

	(r'^api/page/form/$', 'api_widget_form'),
)
