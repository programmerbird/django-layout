# threadlocals middleware
try:
	from threading import local
except ImportError:
	from django.utils._threading_local import local

import settings 

_thread_locals = local()
def get_current_user():
	return getattr(_thread_locals, 'user', None)

def get_request():
	return getattr(_thread_locals, 'request', None)
	
def set_current_user(user):
	_thread_locals.user = user

def get_current_language():
	return getattr(_thread_locals, 'language_code', None)
	
class ThreadLocals(object):
	"""Middleware that gets various objects from the
	request object and saves them in thread local storage."""
	def process_request(self, request):
		if request.user.is_anonymous():
			request.user.id = 0
			request.user.__unicode__ = lambda : r'0'
		_thread_locals.user = getattr(request, 'user', None)
		_thread_locals.request = request
		_thread_locals.language_code = getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)

