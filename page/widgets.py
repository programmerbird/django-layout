#-*- coding:utf-8 -*-


import os
from django import forms
from django.conf import settings 
from django.template.loader import get_template
from django.template import Template, Context
from django.utils import simplejson as json
from django.utils.safestring import mark_safe

from sandbox import parse_variable, render_expression
from hibird.utils import parse_text

from models import *


class Widget(forms.Form):
	def __init__(self, context={}, storage={}, *args, **kwargs):
		super(Widget, self).__init__(*args, **kwargs)
		self.storage = storage
		self.containers = {}
		self.context = {}
		for k,field in self.fields.items():
			self.context[k] = field.initial
			setattr(self, k, field.initial)
		if context:
			self.load_context(context)
	
	def variable(self, expression):	
		return parse_variable(expression, self.storage)
		
	def expression(self, statement, variables=None):
		if variables:
			try:
				self.storage.push()
				for k,v in variables.items():
					self.storage[k] = v 
				return render_expression(statement, self.storage)	
			finally:
				self.storage.pop()
		else:
			return render_expression(statement, self.storage)	
		

	def html(self, request):
		return u""""""
			
	def render(self, request):
		try:
			from django.template import Context, loader
			try:
				from current_user import get_current_user
				if self.Meta.required_login:
					if not get_current_user().is_authenticated():
						return ""
			except AttributeError:
				pass
			self.storage.push()
			try:
				self.storage['context'] = dict([ (k, getattr(self, k, v)) for k,v in self.context.items() ])
				self.storage['widget'] = self
				d = self.html(request)
				if isinstance(d, basestring):
					t = Template(d)
				else:
					t = loader.get_template(self.Meta.template)
					self.storage.update(d)
				return t.render(Context(self.storage))
			finally:
				self.storage.pop()
		except:
			if settings.TEMPLATE_DEBUG:
				import traceback
				traceback.print_exc()
			return ''
			
	def get_value(self, name):
		try:
			return self.context[name]
		except:
			return self.fields[name].initial	
	
	def load_context(self, context):
		for k,v in context.items():
			setattr(self, k, v)
		self.context = context
		
	def get_initial(self):
		result = {}
		for fieldname, field in self.fields.items():
			if field.initial:
				result[fieldname] = field.initial 
		return result
		
	def get_help(self):
		return self.__doc__
		
	def __unicode__(self):
		return self.render()

class Header(Widget):
	url = forms.CharField(required=False, initial="{{ entity.get_absolute_url }}")
	title = forms.CharField(required=False, initial="{{ entity }}")
	
	def get_absolute_url(self):
		if self.url:
			return self.expression(self.url)
			
	def parsed_title(self):
		return self.expression(self.title)
		
	def html(self, request):
		return """
			{% if widget.url %}
				<h1><a href="{{ widget.get_absolute_url }}">{{ widget.parsed_title }}</a></h1>
			{% else %}
				<h1>{{ widget.parsed_title }}</h1>
			{% endif %}
		"""
		
	class Meta:
		pass 

class Login(Widget):
	"""
	Show login information for the current user.
	"""
	welcome_message = forms.CharField(required=False, initial='<a href="{{ request.user.get_absolute_url }}"><strong>{{ request.user }}</strong></a>.')
	guest_message = forms.CharField(required=False, initial="")
	
	def parsed_welcome(self):
		return mark_safe(self.expression(self.welcome_message))
		
	def parsed_guest(self):
		return mark_safe(self.expression(self.guest_message))
		
	def html(self, request):
		return """
			<div id="account">
				{% if request.user.is_authenticated %}
					{{ widget.parsed_welcome }}
					<a href="/accounts/logout">Logout</a>
				{% else %}
					{{ widget.parsed_guest }}
					<a href="/accounts/login">Login</a>
				{% endif %}
			</div>
		"""

	class Meta:
		icon = "%spage/password.png" % settings.MEDIA_URL
		

class Markdown(Widget):
	content = forms.CharField(
		label = '',
		required = False,
		widget = forms.Textarea(
			attrs={'rows': 12, 'class': 'expandable markdown'}
		))
	
	def parsed_content(self):
		return parse_text(self.expression(self.content or ''), application='MARK')
	
	def html(self, request):
		return """
			<div class="text-content">{{ widget.parsed_content }}</div>
		"""
		
	class Meta:
		icon = "%spage/textarea.png" % settings.MEDIA_URL

