#-*- coding:utf-8 -*-
from django.conf import settings 
from hibird.utils import import_class 

class LayoutDoesNotExist(Exception):
	pass 
			
class EntityDoesNotExist(Exception):
	pass 
	
class WidgetDoesNotExist(Exception):
	pass 

DEFAULT_WIDGET_LOADERS = (
	'page.loaders.PathWidgetLoader', 
)
DEFAULT_ENTITY_LOADERS = (
	'page.loaders.SafeModelLoader',
)
DEFAULT_LAYOUT_LOADERS = (
	'page.loaders.SlugLayoutLoader', 
	'page.loaders.EntityLayoutLoader', 
	'page.loaders.EntityTypeLayoutLoader', 
)

LAYOUT_LOADERS = [ import_class(s)() for s in getattr(settings, 'PAGE_LAYOUT_LOADERS', DEFAULT_LAYOUT_LOADERS) ]
ENTITY_LOADERS = [ import_class(s)() for s in getattr(settings, 'PAGE_ENTITY_LOADERS', DEFAULT_ENTITY_LOADERS) ]
WIDGET_LOADERS = [ import_class(s)() for s in getattr(settings, 'PAGE_WIDGET_LOADERS', DEFAULT_WIDGET_LOADERS) ]

def get_layout(slug, entity_type, entity):
	for loader in LAYOUT_LOADERS:
		try:
			result = loader.get(slug=slug, entity_type=entity_type, entity=entity)
			if result:
				return result 
		except:
			pass
	raise LayoutDoesNotExist
	
def filter_entities(entity_type, **kwargs):
	for loader in ENTITY_LOADERS:
		try:
			result = loader.filter(entity_type, **kwargs)
			if result != None:
				return result 
		except:
			pass
	
def get_entity(entity_type, **kwargs):
	try:
		return filter_entities(entity_type, **kwargs)[0]
	except:
		raise EntityDoesNotExist
		
def get_widget(widget_name):
	for loader in WIDGET_LOADERS:
		try:
			result = loader.get(widget_name)
			if result:
				return result 
		except:
			pass
	raise WidgetDoesNotExist(widget_name)
			
def list_widget_names():
	result = []
	for loader in WIDGET_LOADERS:
		result += loader.list()
	return result 

def widget(template, context=False, **kwargs):
	preserved_meta = kwargs
	preserved_meta['template'] = template
	def wrapper(method):
		from widgets import Widget 
		class ViewWidget(Widget):
			def html(self, request):
				from django.template import Context, loader
				if context:
					c = Context(self.storage)
					return method(request, c)
				else:
					return method(request)
		class DictObj:
			def __init__(self, dic):
				for k,v in dic.items():
					setattr(self, k, v)
		ViewWidget.Meta = DictObj(preserved_meta)
		return ViewWidget
		
	return wrapper

