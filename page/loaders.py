#-*- coding:utf-8 -*-

from django.conf import settings 
from hibird.utils import import_class, load_module

WIDGET_PATHS = getattr(settings, 'PAGE_WIDGET_PATHS', [])


""" Default Layout loaders """
class SlugLayoutLoader:
	def get(self, slug=None, entity_type=None, entity=None):
		from models import Layout
		return Layout.objects.get(slug=slug, entity_type=entity_type)
		
class EntityLayoutLoader:
	def get(self, slug=None, entity_type=None, entity=None):
		if hasattr(entity, "layout"):
			return entity.layout 

class EntityTypeLayoutLoader:
	def get(self, slug=None, entity_type=None, entity=None):
		from models import Layout
		return Layout.objects.get(slug="base", entity_type=entity_type)
		

""" Default Entity Loaders """
class SafeModelLoader:
	def filter(self, entity_type, **kwargs):
		if entity_type=='user':
			from models import User
			return User.objects.filter(**kwargs)



""" Default Widget Loaders """
class PathWidgetLoader: 
	def get(self, widget_name):
		for path in WIDGET_PATHS:
			try:
				return import_class("%s.%s" % (path, widget_name))
			except:
				pass 
				
	def list(self,):
		try:
			return self.cache_list 
		except:
			result = []
			for path in WIDGET_PATHS:
				widgets = load_module(path)
				for x in dir(widgets):
					o = getattr(widgets, x)
					if hasattr(o, 'render') and hasattr(o, 'Meta'):
						result.append(x)
			self.cache_list = result 
			return result
			
