#-*- coding:utf-8 -*-

from page.widgets import Widget

class Debug(Widget):
	"""
	Display debug panel on the bottom right of each page.
	Only to superuser of course!
	"""
	def html(self, request):
		layout = self.storage['__layout__']
		layout_slug = layout.slug
		try:
			layout_slug = request.user.custom_page_layout_name[0]
		except:
			pass 
		return """
			{% load i18n %}
			{% if request.user.is_superuser %}
				<div id="debug" style="position: fixed; bottom: 10px; right: 10px">
					{% if flatpage %}
						{% trans "flatpage" %}: 
						<a href="{% url publisher.views.edit_flatpage flatpage.pk %}">{{ flatpage.title }}</a>
					{% else %}
						{% trans "layout" %}: 
						<a href="{% url publisher.views.edit_layout \"""" + str(layout_slug) + """\" %}">""" + layout_slug + """</a>
					{% endif %}
				</div>
			{% endif %}
		"""
	class Meta:
		pass

