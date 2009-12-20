#-*- coding:utf-8 -*-


import time
import datetime
import urllib
import hashlib
from django import template
from django.template import Variable
from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe
from django.utils.tzinfo import LocalTimezone
from django.utils.translation import ungettext, ugettext

register = template.Library()

@register.simple_tag
def inspect(obj):
	print dir(obj)
	
@register.simple_tag
def user(user, title="user: %(username)s"):
	try:
		from django.contrib.auth.models import User
		user = User.objects.get(pk=int(user))
	except:
		pass 

	try:
		username = user.username
		name = user.get_full_name() or username
		url = user.get_absolute_url()
		title = title % user.__dict__
		return '<a href="%(url)s" title="%(title)s">%(name)s</a>' % locals()
	except:
		return ''
		
@register.simple_tag
def shortuser(user):
	try:
		from django.contrib.auth.models import User
		user = User.objects.get(pk=int(user))
	except:
		pass 

	try:
		username = user.username
		if user.is_authenticated():
			if user.first_name and user.last_name:
				name = user.first_name + ' ' + user.last_name[0] + '.'
			elif user.first_name:
				name = user.first_name 
			else:
				name = user.username
		else:
			name = username
		url = user.get_absolute_url()
		title = u"user: %s" % name
		return '<a href="%(url)s" class="user" title="%(title)s">%(name)s</a>' % locals()
	except:
		return ''
		

class SearchUrlNode(Node):
	def __init__(self, key, value):
		self.key = key
		self.value = Variable(value)
 
	def render(self, context):
		key = self.key 
		value = self.value
		try:
			value = self.value.resolve(context)
		except:
			pass
		request = context['request']
		m = dict([ (x, request.GET.get(x)) for x in request.GET.keys() ])
		m[key] = value 
		if 'info' in m:
			del m['info']
		return request.get_full_path().split("?",1)[0] +"?" + '&'.join(['%s=%s' % x for x in m.items() if x[1]!='' ])
		
def searchurl(parser, token):
	try:
		bits = token.split_contents()
	except ValueError:
		raise TemplateSyntaxError('tag requires exactly two arguments')
	if len(bits) != 3:
		raise TemplateSyntaxError('tag requires exactly two arguments')
	return SearchUrlNode(bits[1], bits[2])
register.tag('searchurl', searchurl)

class SearchLinkNode(SearchUrlNode):
	def render(self, context):
		url = super(SearchLinkNode, self).render(context)
		cls = ''
		value = self.value
		try:
			value = self.value.resolve(context)
		except:
			pass 
		if context['request'].GET.get(self.key)==value or (self.key not in context['request'].GET and value==''):
			cls = ' class="selected"'
		return '<a href="%s"%s>' % (url, cls)
 
def searchlink(parser, token):
	try:
		bits = token.split_contents()
	except ValueError:
		raise TemplateSyntaxError('tag requires exactly two arguments')
	if len(bits) != 3:
		raise TemplateSyntaxError('tag requires exactly two arguments')
	return SearchLinkNode(bits[1], bits[2])
register.tag('searchlink', searchlink)

		
@register.filter
def hash(h, key):
	try:
		return h[key]
	except:
		pass 
	try:
		return getattr(h, key)
	except: 
		pass 
	return ''

@register.filter
def parse_text(value):
	from ..hibird.utils import parse_text as parser
	return parser(value)
	
@register.filter('reverse')
def do_reverse(h):
	h = list(h)
	h.reverse()
	return h

@register.filter
def in_list(value, arg):
	return value in arg

@register.filter
def extract(value, arg):
	return [ getattr(x,arg) for x in value ]

@register.filter
def lt(value, arg):
	return value < arg 

@register.filter
def lte(value, arg):
	return value <= arg 

@register.filter
def gt(value, arg):
	return lt(arg, value)

@register.filter
def gte(value, arg):
	return lte(arg, value)
	
@register.filter
def humanize(value):
	import re
	return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', ' \\1', value.replace('_',' ')).lower().strip()
	
@register.filter
def installed(value):
	import settings
	return 	value in settings.INSTALLED_APPS
	
@register.filter
def lstrip(value, strip):
	return value.lstrip(strip)

@register.filter 
def nbspace(value):
	return value.replace("  ", "&nbsp; ")

@register.filter
def shortdate(value):
	try:
		now = datetime.datetime.now()
		if value.date()==value.today().date():
			format = "%l:%M %P"
		elif value.year == value.today().year:
			format = "%b %d"
		else:
			format = "%b %d, %Y"
		display = value.strftime(format)
		if display=='12:00 am':
			display = 'Today'
		q = '<abbr title="%s">%s</abbr>' % (value.strftime("%b %d, %Y @ %l:%M%P"), display)
		return mark_safe(q)	
	except:
		return ''	
		

@register.filter
def longdate(value):
	try:
		now = datetime.datetime.now()
		if value.date()==value.today().date():
			format = "%l:%M %P"
		elif value.year == value.today().year:
			format = "%b %d at %l:%M %P"
		else:
			format = "%b %d, %Y at %l:%M %P"
		display = value.strftime(format)
		if display=='12:00 am':
			display = 'Today'
		q = '<abbr title="%s">%s</abbr>' % (value.strftime("%b %d, %Y @ %l:%M%P"), display)
		return mark_safe(q)	
	except:
		return ''	

@register.filter
def actives(value):
	return value.filter(is_active=True)
	
@register.filter
def totalminutesformat(d):
	"""
	Takes two datetime objects and returns the time between d and now
	as a nicely formatted string, e.g. "10 minutes".  If d occurs after now,
	then "0 minutes" is returned.

	Units used are years, months, weeks, days, hours, and minutes.
	Seconds and microseconds are ignored.  Up to two adjacent units will be
	displayed.  For example, "2 weeks, 3 days" and "1 year, 3 months" are
	possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.

	Adapted from http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
	"""
	chunks = (
	  (60 * 60 * 24 * 365, lambda n: ungettext('year', 'years', n)),
	  (60 * 60 * 24 * 30, lambda n: ungettext('month', 'months', n)),
	  (60 * 60 * 24 * 7, lambda n : ungettext('week', 'weeks', n)),
	  (60 * 60 * 24, lambda n : ungettext('day', 'days', n)),
	  (60 * 60, lambda n: ungettext('hour', 'hours', n)),
	  (60, lambda n: ungettext('minute', 'minutes', n))
	)
	# ignore microsecond part of 'd' since we removed it from 'now'
	since = d * 60
	if since <= 0:
		# d is in the future compared to now, stop processing.
		return u'0 ' + ugettext('minutes')
	for i, (seconds, name) in enumerate(chunks):
		count = since // seconds
		if count != 0:
			break
	s = ugettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}
	if i + 1 < len(chunks):
		# Now get the second item
		seconds2, name2 = chunks[i + 1]
		count2 = (since - (seconds * count)) // seconds2
		if count2 != 0:
			s += ugettext(', %(number)d %(type)s') % {'number': count2, 'type': name2(count2)}
	return s
	

class PageNode(template.Node):
	def __init__(self):
		pass
	def render(self, context):
		return ''
		
class PartialNode(template.Node):
	def __init__(self, name, nodelist, only=False):
		self.name = name 
		self.only = only
		self.nodelist = nodelist
		self.is_partial = False
			
	def render(self, context):
		out = ''
		if not self.is_partial:
			out += '<div class="PARTIAL %s"' % self.name
			out += '>'
		if not self.only or self.is_partial:
			out += self.nodelist.render(context)
		if not self.is_partial:
			out += '</div>'
		return out 

class PartialViewNode(PartialNode):
	def __init__(self, view_name, view_args, target_name, alias_name, index, nodelist):
		self.view_name = view_name 
		self.view_args = [Variable(x) for x in view_args ]
		self.target_name = target_name
		self.alias_name = alias_name or target_name
		self.name = alias_name
		if index is not None:
			self.index = Variable(index)
		else:
			self.index = None
		self.nodelist = nodelist
		self.is_partial = False
		
	def render(self, context):
		from django.core.urlresolvers import reverse
		alias_name = self.alias_name
		if '.views.' not in self.view_name:
			try:
				self.view_name = Variable(self.view_name).resolve(context)
			except:
				pass
		if "/" in self.view_name:
			url = self.view_name
		else:
			url = reverse(self.view_name, args=[x.resolve(context) for x in self.view_args ])
		if self.index is not None:
			alias_name += '-%s' % self.index.resolve(context)
		out = ''
		if not self.is_partial:
			out += '<div class="PARTIAL %s"' % alias_name
			out += ' title="%s#%s"' % (url, self.target_name)
			out += '>'
		out += self.nodelist.render(context)
		if not self.is_partial:
			out += '</div>'
		return out 

@register.tag 
def partial(parser, token, only=False):
	bits = token.contents.split()
	if len(bits) != 2 and len(bits) != 4:
		raise TemplateSyntaxError, "%s tag takes exactly one arguments or 3 arguments" % bits[0]
		
	page_name = bits[1]	
	if len(bits) == 2:
		nodelist = parser.parse(('endpartial',))
		parser.delete_first_token()
		return PartialNode(page_name, nodelist, only=only)
	elif len(bits) == 4:
		template_name = bits[3]
		t = template.loader.get_template(template_name)
		return PartialNode(page_name, t, only=only)
		
def partial_only(parser, token):
	return partial(parser, token, only=True)

register.tag('partial-only', partial_only)
register.tag('partialonly', partial_only)

def partial_from(parser, token):
	"""
		{% partial-from social.views.edit_display user.pk import form as display-form %}
	"""
	bits = token.contents.split()
	target_name = None
	alias_name = None
	index = None
	if bits[-2]=='with':
		index = bits[-1]
		bits = bits[:-2]
	if bits[-2]=='as':
		alias_name = bits[-1]
		bits = bits[:-2]
		target_name = alias_name
	if bits[-2]=='import':
		target_name = bits[-1]
		bits = bits[:-2]
		alias_name = alias_name or target_name
	if not target_name:
		raise TemplateSyntaxError, "invalid %s tag: partial-form [view-name] ([view-args]) import [partial-name] (as [name] (with [number]))" % bits[0]
		
	nodelist = parser.parse(('endpartial',))
	parser.delete_first_token()
		
	view_name = bits[1]
	view_args = bits[2:]
	return PartialViewNode(view_name, view_args, target_name, alias_name, index, nodelist)
	
register.tag('partial-from', partial_from)
register.tag('partialfrom', partial_from)

class JavascriptNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist
		
	def render(self, context):
		from current_user import get_current_user
		user = get_current_user()
		if not hasattr(user, '__templatejs__'):
			user.__templatejs__ = []
		out = self.nodelist.render(context)
		user.__templatejs__.append(out.strip())
		return '' 

@register.tag('javascript')
def javascript(parser, token):
	nodelist = parser.parse(('endjavascript',))
	parser.delete_first_token()
	return JavascriptNode(nodelist)

class PrintJavascriptNode(template.Node):
	def render(self, context):
		from current_user import get_current_user
		user = get_current_user()
		if hasattr(user, '__templatejs__'):
			js = user.__templatejs__
			return "\n".join(js)
		return ''

@register.tag('printjavascript')
def printjavascript(parser, token):
	return PrintJavascriptNode()


class ApiNode(template.Node):
	def __init__(self, view_name, obj, attr):
		self.view_name = view_name
		self.obj = obj 
		self.attr = attr 
	
	def render(self, context):
		from django.core.urlresolvers import reverse
		model = Variable(self.obj).resolve(context)
		entity_type = model.__class__.__name__.lower()
		if self.attr:
			return reverse(self.view_name, args=[entity_type, model.pk, self.attr])
		else:
			return reverse(self.view_name, args=[entity_type, model.pk])

@register.tag
def api(parser, token):
	bits = token.contents.split()
	if len(bits) != 3:
		raise TemplateSyntaxError, "%s tag takes exactly two arguments" % bits[0]
	(tag, view_name, edit_name) = bits
	if '.' in edit_name:
		(obj, attr) = edit_name.split('.', 1)
	else:
		obj = edit_name
		attr = None 
	return ApiNode(view_name, obj, attr)
	
@register.tag
def layout(parser, token):
	try:
		from current_user import get_current_user
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
def layout_expression(parser, token):
	try:
		from current_user import get_current_user
		bits = token.contents.split()
		if len(bits) != 2:
			raise TemplateSyntaxError, "%s tag takes exactly one arguments" % bits[0]
		page_name = bits[1]
		user = get_current_user()
		if not hasattr(user, 'custom_page_layout_name'):
			user.custom_page_layout_name = []
		user.custom_page_layout_name.append('=' + page_name)
		return PageNode()
	except:
		pass

@register.filter
def truncatechars(value, arg):
	length = int(arg)
	value = unicode(value)
	if len(value) > length:
		return value[:length] + "..."
	else:
		return value 	

