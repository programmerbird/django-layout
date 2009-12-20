#-*- coding:utf-8 -*-


import urllib, hashlib
from django.conf import settings
from django import template

register = template.Library()
DEFAULT_HASH = getattr(settings, 'DEFAULT_GRAVATAR_HASH', 'ad516503a11cd5ca435acc9bb6523536') # unknown@gravatar.com

def get_url(email,size=48):
	from django.contrib.auth.models import User
	if "social" in settings.INSTALLED_APPS:
		if isinstance(email, User):
			from social.models import Preference
			user = email 
			pref = Preference.get(user)
			if pref.picture:
				if int(size)==22:
					return pref.picture.url_22x22
				elif int(size)==200:
					return pref.picture.url_200
				else:
					return pref.picture.url_48x48
					
	if "people" in settings.INSTALLED_APPS:
		o = email
		from people.models import Contact, Company
		if isinstance(o, User):
			user = email 
			o = Contact.get(user)
		if isinstance(o, Contact) or isinstance(o, Company):
			if o.picture:
				if int(size)==22:
					return o.picture.url_22x22
				elif int(size)==200:
					return o.picture.url_200
				else:
					return o.picture.url_48x48
					
	if hasattr(email, 'email'):
		email = email.email 
	try:
		email = User.objects.get(pk=int(email)).email
	except:
		pass 
	defaulthash = DEFAULT_HASH
	try:
		emailhash = hashlib.md5(email).hexdigest()
		url = "http://www.gravatar.com/avatar/%(emailhash)s.jpg?" % locals()
		url += urllib.urlencode({
			's': str(size),
			'd': 'http://www.gravatar.com/avatar/%(defaulthash)s?s=%(size)s' % locals(),
		})
	except:
		url = 'http://www.gravatar.com/avatar/%(defaulthash)s?s=%(size)s' % locals()
	return url				

@register.simple_tag
def gravatar(email, size=48):
	"""
	Simply gets the Gravatar for the commenter. There is no rating or
	custom "not found" icon yet. Used with the Django comments.
	
	If no size is given, the default is 48 pixels by 48 pixels.
	
	Template Syntax::
	
		{% gravatar comment.user_email [size] %}
		
	Example usage::
		
		{% gravatar comment.user_email 48 %}
	
	"""
	url = get_url(email, size)
	return """<img src="%s" width="%s" height="%s" alt="gravatar" class="gravatar" border="0" />""" % (url, size, size)

