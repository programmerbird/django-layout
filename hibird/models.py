#-*- coding:utf-8 -*-

import re 
from django.db import models

class SlugNotCorrectlyPrePopulated(Exception): 
	pass 

def string_to_slug(s):	
	raw_data = s
	# normalze string as proposed on http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/251871
	# by Aaron Bentley, 2006/01/02
	try:
		import unicodedata		
		raw_data = unicodedata.normalize('NFKD', raw_data.decode('utf-8', 'replace')).encode('ascii', 'ignore')
	except:
		pass
	return re.sub(r'[^a-z0-9-]+', '-', raw_data.lower()).strip('-')
	
# as proposed by Archatas (http://www.djangosnippets.org/users/Archatas/)
def _get_unique_value(model, proposal, field_name="slug", instance_pk=None, separator="-"):
	""" Returns unique string by the proposed one.
	Optionally takes:
	* field name which can  be 'slug', 'username', 'invoice_number', etc.
	* the primary key of the instance to which the string will be assigned.
	* separator which can be '-', '_', ' ', '', etc.
	By default, for proposal 'example' returns strings from the sequence:
		'example', 'example-2', 'example-3', 'example-4', ...
	"""
	if instance_pk:
		similar_ones = model.objects.filter(**{field_name + "__startswith": proposal}).exclude(pk=instance_pk).values(field_name)
	else:
		similar_ones = model.objects.filter(**{field_name + "__startswith": proposal}).values(field_name)
	similar_ones = [elem[field_name] for elem in similar_ones]
	if proposal not in similar_ones:
		return proposal
	else:
		numbers = []
		for value in similar_ones:
			match = re.match(r'^%s%s(\d+)$' % (proposal, separator), value)
			if match:
				numbers.append(int(match.group(1)))
		if len(numbers)==0:
			return "%s%s2" % (proposal, separator)
		else:
			largest = sorted(numbers)[-1]
			return "%s%s%d" % (proposal, separator, largest + 1)
			
SLUGIFICATION_METAS = (
	'Slugification', 
	'SlugMeta', 
	'DefaultFormMeta'
)
def _get_fields_and_data(model):
	opts = model._meta
	slug_fields = []
	
	for META in SLUGIFICATION_METAS:
		if hasattr(model, META):
			ns = getattr(model, META).prepopulated_fields
	for f in opts.fields:
		if f.name not in ns:
			continue
		if isinstance(f, models.SlugField):
			unique = True
		else:
			unique = False
		try:
			if len(ns) == 0:
				raise Exception("Nothing found")
		except Exception, e:
			raise SlugNotCorrectlyPrePopulated , "Slug for %s is not prepopulated %s " % (f.name, e)
		prepop = []
		for n in ns[f.name]:
			if not hasattr(model, n):
				raise SlugNotCorrectlyPrePopulated , "Slug for %s is to be prepopulated from %s, yet %s.%s does not exist" % (f.name , n , type(model), n)
			else:
				prepop.append(getattr(model, n) or '')
		slug_fields.append([f , "_".join(prepop), unique])
	return slug_fields
	
def slugify(sender, instance, signal, *args, **kwargs):	
	for slugs in _get_fields_and_data(instance):	
		(field, original, unique) = slugs
		original_slug = string_to_slug(original)
		slug = getattr(instance, field.name) or original_slug or 'item'
		ct = 0;
		try:
			# See if object is new
			# To prevent altering urls, don't update slug on existing objects
			sender.objects.get(pk=instance._get_pk_val())
		except:
			if unique:
				slug = _get_unique_value(instance.__class__, slug, field.name, separator="-")
			elif not slug:
				slug = original_slug
			setattr(instance, field.name, slug)

class ActiveObjectManager(models.Manager):
	def get_query_set(self):
		return super(ActiveManager, self).get_query_set().filter(is_active=True)

def fill_default(sender=None, instance=None, created=False, **kwargs):
	try:
		from current_user import get_current_user, get_request
		import datetime
		if hasattr(instance, 'owner'):
			if not instance.owner:
				u = get_current_user()
				if u and u.is_authenticated():
					instance.owner = u 
					
		if hasattr(instance, 'owner_ip'):
			if not instance.owner_ip:
				request = get_request()
				instance.owner_ip = request.META['REMOTE_ADDR']
				
		if hasattr(instance, 'created_on'):
			if not instance.created_on:
				instance.created_on = datetime.datetime.now()
			
		if hasattr(instance, 'updater'):
			u = get_current_user()
			if u and u.is_authenticated():
				instance.updater = u 

		if hasattr(instance, 'updated_on'):
			instance.updated_on = datetime.datetime.now()
	except:
		pass
		
# ===========================
# To attach it to your model:
# ===========================
# dispatcher.connect(_package_.slugify, signal=signals.pre_save, sender=_your_model_)


from django.db import connection

def query_to_dicts(query_string, *query_args):
    """Run a simple query and produce a generator
    that returns the results as a bunch of dictionaries
    with keys for the column values selected.
    """
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    col_names = [desc[0] for desc in cursor.description]
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        yield row_dict
    return
    
def find_object(finders, name):
	for finder in finders:
		try:
			result = finder(name)
			if isinstance(result, models.Model):
				return result 
			else:
				for x in result:
					return x
		except:
			pass 

def filter_objects(finders, name, min_result=5):
	left = min_result
	result = []
	for finder in finders:
		if left <= 0:
			return result 
		try:
			r = finder(name)
			if isinstance(r, models.Model):
				if r not in result:
					result.append(r)
					left -= 1
			else:
				for x in r:
					if x not in result[:left+1]:
						result.append(x)
						left -= 1
		except:
			pass 			
	return result


