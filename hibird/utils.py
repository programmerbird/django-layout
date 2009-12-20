#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django import forms

from django.conf import settings
import random
import re


DEBUG = getattr(settings, 'DEBUG', False)
PARSER_PLUGINS = getattr(settings, 'PARSER_PLUGINS', []) 
DEFAULT_PARSER = getattr(settings, 'DEFAULT_PARSER', 'MARK')

def _remove_guest_fields_if_authen(form):
	from current_user import get_request
	request = get_request()
	if request.user.is_authenticated():
		for k,v in form.fields.items():
			if k.startswith('guest_'):	
				del form.fields[k]

def _remove_unprivilege_fields(form):
	try:
		fields = form.instance.Meta.EditPermissionFields
		for fnct,attrs in fields:
			if getattr(form.instance, fnct)():
				continue
			for x in attrs:
				if x in form.fields:
					del form.fields[x]
	except:
		pass 
	
def Form(form_type, request=None, **kw):
	from current_user import get_request
	request = get_request()
	if isinstance(form_type, HttpRequest):	# backward compat
		(request, form_type) = (form_type, request)
	
	class _FormWrapper(form_type):	
		def __init__(self, *args, **kwargs):
			super(_FormWrapper, self).__init__(*args, **kwargs)
			_remove_guest_fields_if_authen(self)
			_remove_unprivilege_fields(self)
	if request.method=='POST' and not request.GET.get('PARTIAL'):
		return _FormWrapper(data=request.POST, files=request.FILES, **kw)
	else:
		return _FormWrapper(**kw)

def load_module(definition):
	module = __import__(definition)	
	components = definition.split('.')
	for component in components[1:]:
		module = getattr(module, component)
	return module
	
def import_class(definition):
	if isinstance(definition, basestring):
		components = definition.split('.')
		module = load_module('.'.join(components[:-1]))
		return getattr(module, components[-1])
	return definition


def raise_form_error(form):
	import re
	STRIP_HTML = re.compile(ur'\<[^\>]*\>')
	for field in form:
		for error in field.errors:
			raise Exception(STRIP_HTML.sub('', unicode(error).replace('This field', unicode(field.label))))
	if isinstance(form.non_field_errors, basestring):
		raise Exception (STRIP_HTML.sub('', unicode(form.non_field_errors)))
	else:
		raise Exception (STRIP_HTML.sub('', unicode(form.non_field_errors[0])))
		
def handle_ajax_call(request, output):
	if isinstance(output, dict): 
		if 'form' in output:
			form = output['form']
			if not form.is_valid() or form.non_field_errors:
				raise_form_error(form)
	return HttpResponse("OK", status=200)	

def render_to(template):
	"""
	Decorator for Django views that sends returned dict to render_to_response function
	with given template and RequestContext as context instance.

	If view doesn't return dict then decorator simply returns output.
	Additionally view can return two-tuple, which must contain dict as first
	element and string with template name as second. This string will
	override template name, given as parameter

	Parameters:

	 - template: template name to use
	"""
	def renderer(func):
		def wrapper(request, *args, **kw):
			if '__hibird_ajax' in request.GET:
				try:
					output = func(request, *args, **kw)
					return handle_ajax_call(request, output)
				except Exception, e:
					return HttpResponse(unicode(e), status=400)
			else:
				from django.core.exceptions import PermissionDenied
				from django.contrib.auth.decorators import login_required
				try:
					output = func(request, *args, **kw)
				except PermissionDenied:
					if not request.user.is_authenticated():
						@login_required
						def wrapper(request):
							raise PermissionDenied
						return wrapper(request)
					raise PermissionDenied
			context = RequestContext(request)
			context['keywords'] = kw
			context['args'] = args
			if isinstance(output, (list, tuple)):
				return render_to_response(output[1], output[0], context)
			elif isinstance(output, dict):
				if not ('PARTIAL' in request.GET and request.method=='GET'):
					return render_to_response(template, output, context)
				else:
					context.update(output)
					from django.template import loader 
					from django.templatetags.hibird import PartialNode
					t = loader.get_template(template)
					block_name = request.GET.get('PARTIAL')
					for node in t.nodelist:
						if isinstance(node, PartialNode):
							if node.name == block_name:
								node.is_partial = True
								return HttpResponse(node.render(context))
						blocks = node.get_nodes_by_type(PartialNode)
						for n in blocks:
							if n.name == block_name:
								n.is_partial = True
								return HttpResponse(n.render(context))
					raise Exception("Invalid block name")
			return output
		return wrapper
	return renderer


def random_string(length):
	return ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for x in xrange(length)])


def urlencode(value, safe='/'):
	"Escapes a value for use in a URL"
	try:
		import urllib
		return urllib.quote(value, safe)
	except:
		return value

def uri(*args, **kwargs):
	
	url = None
	flowArgs = None
	for v in args:
		if isinstance(v, dict):
			kwargs = v
		if isinstance(v, basestring):
			url = v
		if isinstance(v, list):
			flowArgs = [ unicode(x) for x in v if x is not None ]
	
	if '/' in url:
		pass
	else:
		url = reverse(url, args=flowArgs)
		
	if kwargs is not None:
		qmap = {}
		sharp = None
		for k,v in kwargs.items():
			if k=='#' or k=='_target':
				sharp = v 
			else:
				qmap[k] = v
		
		if qmap:
			url = url + ('&' if '?' in url else '?')
			url = url + '&'.join([ "%s=%s" % (k, urlencode(v)) for k,v in qmap.items()])
		
		if sharp:
			url = url + '#' + sharp
	return url
	
def redirect(*args, **kwargs):
	from current_user import get_request
	url = None
	request = get_request()
	if 'next' in request.GET:
		url = request.GET.get('next')
	if 'next' in request.POST:
		url = request.POST.get('next')
	if not url:
		url = uri(*args, **kwargs)
	else:
		if 'info' in kwargs:
			qmap = dict([ (x, kwargs.get(x)) for x in "info ask ask_url".split() if kwargs.get(x) ])
			if qmap:
				url = url + ('&' if '?' in url else '?')
				url = url + '&'.join([ "%s=%s" % (k, urlencode(v)) for k,v in qmap.items()])
	return HttpResponseRedirect(url)

def search_in(query, searchstring, columns):
	import shlex
	n = query.none()
	for word in searchstring.split():
		q = n 
		for column in columns:
			q = q | query.filter(**{column + '__icontains': word })
		query = query & q
	return query
	
def query(items, data={}, querymap={}):
	for key,value in data.items():
		if value.strip()=='':
			continue
		if key in querymap:
			fnct = querymap[key]
			try:
				if isinstance(fnct, basestring):
					items = items.filter(**{fnct: value })
				elif callable(fnct):
					items = fnct(items, value)
			except:
				pass
	return items
	
urlfinder = re.compile('^(http:\/\/\S+)')
urlfinder2 = re.compile('\s(http:\/\/\S+)')
def urlify_markdown(value):
	value = urlfinder.sub(r'<\1>', value)
	return urlfinder2.sub(r' <\1>', value)
	
def urlify_pattern_markdown(value):
	patterns = getattr(settings, "URL_PATTERNS", [])
	for pattern,url in patterns:
		replacement = r"[\g<0>](" + url + ")"
		value = re.sub(pattern, replacement, value)
	return value
	
LIST_PATTERN = re.compile(r'^\s*(\d+\s*\.|\*|\#|\-)')
def auto_linebreak_markdown(value):
	result = []
	for x in value.split('\n'):
		if not LIST_PATTERN.match(x):
			x += '  '
		result.append(x)
	return '\n'.join(result)
	
def parse_text(value, application=None):
	value = value or ''
	if not application:
		application = DEFAULT_PARSER
	try:
		from django.utils.encoding import smart_str, force_unicode
		from django.utils.safestring import mark_safe
		value = smart_str(value)
		value = value.strip()
		if application=='TXTL':
			import textile
			value = textile.textile(value, encoding='utf-8', output='utf-8', sanitize=True)
			value = force_unicode(value)
		elif application=='MARK':
			import markdown
			value = force_unicode(value)
			value = auto_linebreak_markdown(value)
			value = urlify_markdown(value)
			value = urlify_pattern_markdown(value)
			value = markdown.markdown(value, safe_mode="escape")
		elif application=='REST':
			from docutils.core import publish_parts
			value = force_unicode(value)
			docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
			parts = publish_parts(source=value, writer_name="html4css1", settings_override=docutils_settings)
			value = parts["fragment"]
		elif application=='HTML':
			value = force_unicode(value)
		for x in PARSER_PLUGINS:
			try:
				value = import_class(x)(value)
			except:
				import traceback
				traceback.print_exc()
		value = mark_safe(value)
	except:
		pass
	return value 
	

def login_as(request, user):
	"""
	Log in a user without requiring credentials (using ``login`` from
	``django.contrib.auth``, first finding a matching backend).
	"""
	from django.contrib.auth import load_backend, login
	if not hasattr(user, 'backend'):
		for backend in settings.AUTHENTICATION_BACKENDS:
			if user == load_backend(backend).get_user(user.pk):
				user.backend = backend
				break
	if hasattr(user, 'backend'):
		return login(request, user)	
	

def permission(can_something):
	from current_user import get_current_user
	def can(self):
		app = self.__class__._meta.app_label
		module = self.__class__._meta.module_name 
		action = can_something.__name__[4:]
		if '_' in action:
			x = '%s.%s' % (app, action)
		else:
			x = '%s.%s_%s' % (app, action, module)
		user = get_current_user()
		if user.has_perm("%s.%s" % (app,x)):
			return True 
		if user.is_authenticated():
			if hasattr(self, 'owner'):
				if user == self.owner:
					return True 
		return can_something(self)
	return can

