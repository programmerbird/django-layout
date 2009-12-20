#-*- coding:utf-8 -*-

from django import forms
from django.contrib.flatpages.models  import FlatPage
from page.models import *


class NewLayoutForm (forms.ModelForm):
	containers = forms.CharField(
		required = False,
		widget = forms.HiddenInput(),
		initial='')
		
	class Meta:
		model = Layout
		exclude = (
			'parent', 
			'template',
			'entity_type',
		)

class EditLayoutForm (NewLayoutForm):
	pass 


class NewFlatPageForm (forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(NewFlatPageForm, self).__init__(*args, **kwargs)
		self.fields['content'].widget.attrs['rows'] = 30
	class Meta:
		model = FlatPage
		exclude = ('sites',)

class EditFlatPageForm (forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(EditFlatPageForm, self).__init__(*args, **kwargs)
		self.fields['content'].widget.attrs['rows'] = 30
	class Meta:
		model = FlatPage
		exclude = ('sites',)

