#-*- coding:utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.flatpages.models  import FlatPage
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from hibird.utils import render_to, redirect, Form
from django.conf import settings
import forms 

from page.utils import get_widget, list_widget_names
from page.models import *

@login_required
@render_to('publisher/layout/list.html')
def layouts(request):
	if not request.user.is_superuser:
		raise PermissionDenied()
	site = Site.objects.get_current()
	layouts = Layout.objects.all().order_by('name')
	pages = FlatPage.objects.filter(sites__pk=site.pk).order_by('title')
	return locals()

@login_required
@render_to('publisher/layout/edit.html')
def edit_layout(request, layout_slug=None):
	if not request.user.is_superuser:
		raise PermissionDenied()
	try:
		layout_id = int(layout_slug)
		layout = Layout.objects.get(pk=int(layout_id))
	except ValueError:
		try:
			layout = Layout.objects.get(slug=layout_slug)
		except Layout.DoesNotExist:
			return redirect('publisher.views.new_layout',
				name = layout_slug.replace('_',' ').title(),
				slug = layout_slug)
	except Layout.DoesNotExist:
		raise Http404
		
	try:
		form = Form(forms.EditLayoutForm, instance=layout)
		if request.method=='POST':
			if form.is_valid():
				n = form.save(commit=False)
				n.save()
				return redirect("publisher.views.edit_layout", [str(n.id)], 
						info = 'Layout "%s" saved successfully' % n.name )
	except Exception, e:
		form.non_field_errors = str(e) or "Please try again later."
	widget_names = list_widget_names()
	widget_names.sort()

	return locals()

@login_required
@render_to('publisher/layout/new.html')
def new_layout(request):
	if not request.user.is_superuser:
		raise PermissionDenied()
	initial = {}
	if request.method=='GET':
		initial = {
			'name': request.GET.get('name',''),
			'slug': request.GET.get('slug',''),
		}
	try:
		form = Form(forms.NewLayoutForm, initial=initial)
		if request.method=='POST':
			if form.is_valid():
				n = form.save(commit=False)
				n.save()
				return redirect("publisher.views.edit_layout", [str(n.id)], 
						info = 'Layout "%s" created successfully' % n.name )
	except Exception, e:
		form.non_field_errors = str(e) or "Please try again later."
	widget_names = list_widget_names()
	widget_names.sort()
	return locals()

@login_required
def remove_layout(request, layout_id, layout_slug=None):
	if not request.user.is_superuser:
		raise PermissionDenied()
	try:
		layout = Layout.objects.get(pk=layout_id)
	except Layout.DoesNotExist:
		raise Http404
	try:
		layout.delete()
		return redirect("publisher.views.layouts", 
					info = 'Layout "%s" removed successfully' % layout.name )
	except Exception, e:
		return redirect("publisher.views.layouts", 
					info = 'Oops! we have a problem with a server, Please try again later',
					error = str(e))
					
					

@render_to('publisher/flatpage/edit.html')
def edit_flatpage(request, flatpage_id):
	if not request.user.is_superuser:
		raise PermissionDenied()
	try:
		flatpage = entity = FlatPage.objects.get(pk=flatpage_id)
	except FlatPage.DoesNotExist:
		raise Http404	
	try:
		form = Form(forms.EditFlatPageForm, instance=flatpage)
		if request.method=='POST':
			if form.is_valid():
				n = form.save(commit=False)
				site = Site.objects.get_current()
				if n.url and not n.url.endswith('/'):
					n.url += '/'
				n.sites.add(site)
				n.save()
				return redirect("publisher.views.edit_flatpage", [str(n.id)], 
					info=_('Saved successfully'))
	except Exception, e:
		form.non_field_errors = unicode(e) or _("Please try again later.")
	return locals()

@render_to('publisher/flatpage/new.html')
def new_flatpage(request):
	if not request.user.is_superuser:
		raise PermissionDenied()
	try:
		form = Form(forms.NewFlatPageForm, initial={})
		if request.method=='POST':
			if form.is_valid():
				n = form.save(commit=False)
				if n.url and not n.url.endswith('/'):
					n.url += '/'
				n.save()
				site = Site.objects.get_current()
				n.sites.add(site)
				n.save()
				return redirect("publisher.views.edit_flatpage", [str(n.id)], 
						info=_('Created successfully'))
	except Exception, e:
		form.non_field_errors = unicode(e) or _("Please try again later.")
	return locals()

def remove_flatpage(request, flatpage_id):
	if not request.user.is_superuser:
		raise PermissionDenied()
	try:
		flatpage = FlatPage.objects.get(pk=flatpage_id)
	except FlatPage.DoesNotExist:
		raise Http404
	error = None
	try:
		flatpage.delete()
		return redirect("publisher.views.layouts", 
					info = _('Removed successfully'))
	except Exception, e:
		error = e
	return redirect("publisher.views.layouts", 
				info = _('Oops! we have a problem with a server, Please try again later'),
				error = unicode(error))


@render_to('publisher/widget/form.html')
def api_widget_form(request, widget_name=None):
	try:
		widget_name = widget_name or request.GET.get('name')
		form = get_widget(widget_name)()	
	except:
		raise Http404 
	return locals()

