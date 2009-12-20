#-*- coding:utf-8 -*-


import time
import datetime
import urllib
import hashlib
from django import template
from django.template import Variable
from django.utils.safestring import mark_safe
from django.utils.tzinfo import LocalTimezone
from django.utils.translation import ungettext, ugettext
from page.models import *

from current_user import get_current_user

register = template.Library()
	
class GetContainerNode(template.Node):
	def __init__(self, container_name, parser=None):
		self.container_name = container_name
		self.parser = parser 
	
	def render(self, context):
		if '_list_containers' in context:
			context['_list_containers'].append(self.container_name)
			return ''

		if '__layout__' not in context:
			user = get_current_user()
			if hasattr(user, 'custom_page_layout_name'):
				t = []
				for x in user.custom_page_layout_name:
					if x.startswith('='):
						x = Variable(x[1:]).resolve(context)
					t.append(x)
				user.custom_page_layout_name = t
				layout = None
				for x in t:
					try:
						layout = Layout.objects.get(slug=x)
						break
					except:
						pass 
				if not layout:
					layout = Layout.get(t[-1])
				if not layout:
					layout = Layout.get('base')
				if layout:
					context['__layout__'] = layout
				
		if '__layout__' not in context: 
			return '' 
			
		if 'entity' not in context:
			user = get_current_user()
			if hasattr(user, 'entity_name'):
				entity = Variable(user.entity_name).resolve(context)
				context['entity'] = entity
				
		layout = context.get('__layout__')
		entity = context.get('entity')
		return layout.render_container(entity, self.container_name, context)
 
@register.tag
def container(parser, token):
	bits = token.contents.split()
	if len(bits) != 2:
		raise TemplateSyntaxError, "%s tag takes exactly one arguments" % bits[0]
	return GetContainerNode(bits[1], parser=parser)

class PageNode(template.Node):
	def __init__(self):
		pass
	def render(self, context):
		return ''

@register.tag
def page(parser, token):
	try:
		bits = token.contents.split()
		if len(bits) != 2:
			raise TemplateSyntaxError, "%s tag takes exactly one arguments" % bits[0]
		page_name = bits[1]
		user = get_current_user()
		if not hasattr(user, 'custom_page_layout_name'):
			user.custom_page_layout_name = []
		user.custom_page_layout_name.append(page_name)
		return PageNode()
	except:
		pass

@register.tag		
def setentity(parser, token):
	try:
		bits = token.contents.split()
		if len(bits) != 2:
			raise TemplateSyntaxError, "%s tag takes exactly one arguments" % bits[0]
		entity_name = bits[1]
		user = get_current_user()
		user.entity_name = entity_name
		return PageNode()
	except:
		pass
	
