#-*- coding:utf-8 -*-

import datetime
import StringIO

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.models import signals
from hibird.models import slugify

from utils import get_widget
from current_user import get_current_user, get_request
from jsonfield import JSONField, dumps as json_dumps, loads as json_loads


DEFAULT_LAYOUT_SLUG = getattr(settings, "DEFAULT_LAYOUT_SLUG", "base")
DEFAULT_LAYOUT_TEMPLATE = getattr(settings, "DEFAULT_LAYOUT_TEMPLATE", "base.html")

	
class Layout (models.Model):
	"""
		layout.containers = {
			'_parent_': {
				'header': [
					('module1', {}),
					('module2', {}),
				],
				'footer': [
					('module1', {}),
					('module2', {}),
				],
			},
			'article': [
				('entry', {}),
				('comment', {}),
			],
		}
	"""
	
	name = models.CharField(verbose_name="Layout Name", max_length=200)
	slug = models.CharField(verbose_name="Layout Slug", max_length=200, null=True, blank=True)
	entity_type = models.CharField(verbose_name="Entity Type", max_length=200, null=True, blank=True)
	
	owner = models.ForeignKey(User, null=True, related_name="layout_owned", editable=False)
	created_on = models.DateTimeField(auto_now_add=True, editable=False)
	updater = models.ForeignKey(User, null=True, related_name="layout_updated", editable=False)
	updated_on = models.DateTimeField(auto_now=True, editable=False)
	
	parent = models.ForeignKey('self', null=True, blank=True)
	template = models.CharField(max_length=200, null=True, blank=True)	
	containers = models.TextField(null=True, blank=True)
	
	is_active = models.BooleanField(default=True, editable=False)
	
	@classmethod
	def get(cls, slug=None):
		if slug:
			slug = slug.replace('/','-').strip('-')
		try:
			return Layout.objects.filter(entity_type='').get(slug=slug)
		except:
			pass 
		try:
			return Layout.objects.filter(entity_type__isnull=True).get(slug=slug)
		except:
			pass 
		try:
			layout = Layout.objects.get(slug=DEFAULT_LAYOUT_SLUG)
			return layout 
		except:
			layout, created = Layout.objects.get_or_create(name="Base", slug=DEFAULT_LAYOUT_SLUG)
			return layout
				
	def get_template(self):
		if self.template:
			return self.template 
		return DEFAULT_LAYOUT_TEMPLATE

	def render_widget(self, entity, context, storage={}):
		(widget_name, widget_context) = context 
		widget = get_widget(widget_name)(context=widget_context, storage=storage) 
		request = get_request()
		return widget.render(request)
	
	def render_container(self, entity, container_name, storage={}):
		try:
			widgets_context = self.get_containers().get(container_name)
			if not widgets_context:
				return ""
			writer = StringIO.StringIO()
			try:
				for widget_context in widgets_context:
					writer.write(self.render_widget(entity, widget_context, storage=storage))
				return writer.getvalue()
			finally:
				writer.close()
		except:
			pass
			
	def get_containers(self):
		try:
			return self._flat_containers
		except:
			try:
				c = json_loads(self.containers or "")
			except ValueError:
				c = {}
			r = dict(c.get('_parent_', {}).items())
			for (k,v) in c.items():
				if k.startswith('_'): continue
				if v:
					r[k] = v 
			self._flat_containers = r 
			return r
			
	def save(self,*args,**kwargs):
		try:
			if not self.parent and self.slug != DEFAULT_LAYOUT_SLUG:
				self.parent = Layout.get()
			if self.parent and self.parent != self:
				try:
					c = json_loads(self.containers or "")
				except ValueError:
					c = {}
				r = dict(self.parent.get_containers().items())
				for (k,v) in c.items():
					if v:
						r[k] = None
						del r[k] 
				if r:
					c['_parent_'] = r 
				self.containers = json_dumps(c)
		except:
			pass
		super(Layout, self).save(*args, **kwargs)
		
		children = Layout.objects.filter(parent=self).exclude(pk=self.pk)
		for child in children:
			child.save()
				
	def __unicode__(self):
		if self.entity_type:
			return "%s / %s" % (self.entity_type, self.slug)
		else:
			return self.name 
		
	class Slugification:
		prepopulated_fields = {'slug': ('name',),}

