#-*- coding:utf-8 -*-


from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

import settings
from models import *
from utils import get_layout, get_entity

def page(request, entity_type, entity_id, layout_slug=None):
	try:
		entity = get_entity(entity_type, pk=int(entity_id))			
	except:
		import traceback
		traceback.print_exc()
		raise Http404
	try:
		__layout__ = get_layout(slug=layout_slug, entity_type=entity_type, entity=entity)
	except:
		__layout__ = Layout.get()
	output = locals()
	context = RequestContext(request)
	return render_to_response(__layout__.get_template(), output, context)



