
# Welcome to django-layout wiki!

A template widgets system for your existed django project.

![Rearrange widgets screenshot](http://github.com/ssimasanti/django-layout/raw/master/doc/edit-base.png)

## Demo
			git clone git://github.com/ssimasanti/django-layout.git
			cd django-layout
			python manage.py runserver

Now goto:
http://localhost:8000/publisher/layout/

Username: admin

Password: admin


## How to implement the custom widget ?

See publisher/widgets.py for the example.
... 


## Installation

1. git clone!

				git clone git@github.com:ssimasanti/django-layout.git

2. Copy the following apps/media files into your project
   - hibird/
   - page/
   - publisher/
   - media/hibird/
   - media/publisher/

3. Add the following lines into your settings.py 

				# [module: hibird]
				INSTALLED_APPS += ('hibird',)
				
				# [module: current_user]
				INSTALLED_APPS += ('current_user',)
				MIDDLEWARE_CLASSES += (
					'current_user.middlewares.ThreadLocals',
				)
				
				# [module: page]
				INSTALLED_APPS += ('page',)
				PAGE_WIDGET_PATHS = (
					'page.widgets',
				)
				
				# [module: publisher]
				INSTALLED_APPS += ('publisher',)
				PAGE_WIDGET_PATHS += (
					'publisher.widgets',
				)


4. Add an URL entry to your project's urls.py, for example:

				urlpatterns += patterns('', 
					(r'^publisher/', include('publisher.urls')), 
				)
   
   
5. That's it. syncdb, runserver and goto http://localhost:8000/publisher/layout/ !

## Usage 

1. Add widget containers into your master template file.
   By default, you will need: header, nav, subnav, intro, article, footnote, aside, footer.
   see templates/hibird.html for the full example.

				{% load page_tags %}		
				<html>
				<body>
					<div id="header">
						{% block header %}{% endblock %}
						{% container header %}
						{% block after-header %}{% endblock %}
					</div>
				</body>
				</html>	

2. Tell us what the layout name. You will have to set it in every pages you want to see the widgets.

				{% load hibird %}
				{% layout your_page_name_here %}

