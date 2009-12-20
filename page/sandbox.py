#-*- coding:utf-8 -*-
from django.template import Variable, Context, Template, RequestContext
from current_user import get_request

def parse_variable(expression, storage={}):
	if expression is None: 
		expression = ''
	request = get_request()
	c = RequestContext(request, storage);
	v = Variable(expression).resolve(c);
	return v
	
def render_expression(expression, storage={}):
	if expression is None: 
		expression = ''
	try:
		if expression.startswith('='):
			rendered = parse_variable(expression[1:], storage)
		else:
			request = get_request()
			c = RequestContext(request, storage)
			t = Template(expression)
			rendered = t.render(c)
		return rendered
	except Exception, e:
		return unicode(e)


