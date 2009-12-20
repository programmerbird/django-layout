from django.db.models import get_apps, get_models, signals
import models 

slugified_model_cache = list()
for app in get_apps():
	for model_class in get_models(app):
		try:
			if getattr(model_class,'Slugification'):
				if not model_class in slugified_model_cache:
					slugified_model_cache.append(model_class)
					signals.pre_save.connect(models.slugify, sender=model_class)

		except AttributeError:
			continue

hibird_model_cache = list()
for app in get_apps():
	for model_class in get_models(app):
		try:
			if model_class in hibird_model_cache:
				continue
			hibird_model_cache.append(model_class)
			for field in model_class._meta.fields:
				if field.name in ('owner', 'updater', 'created_on', 'updated_on') :
					signals.pre_save.connect(models.fill_default, sender=model_class)
					break
		except AttributeError:
			import traceback
			traceback.print_exc()
			continue
