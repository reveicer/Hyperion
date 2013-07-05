# import models
from Hyperion.apps.hcustomers.models import *

# django imports
from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect

class CompanyRegistrationForm(ModelForm):
	# db calls for models
	industry_models = Industry.objects.filter(is_active=True)
	category_models = Category.objects.filter(is_active=True)

	# customized form fields
	industries = forms.ModelMultipleChoiceField(industry_models, widget=forms.CheckboxSelectMultiple(), required=False)
	industry_expertise = forms.ModelMultipleChoiceField(industry_models, widget=forms.CheckboxSelectMultiple(), required=False)
	categories = forms.ModelMultipleChoiceField(category_models, widget=forms.CheckboxSelectMultiple(), required=False)
	category_expertise = forms.ModelMultipleChoiceField(category_models, widget=forms.CheckboxSelectMultiple(), required=False)

	class Meta:
		model = CompanyProfile
		# TODO: missing the core expertise fields
		fields = ('name', 'phone', 'fax', 'email', 'website', 'region', 'primary_type', 'all_types', 'about',
				'street_line1', 'street_line2', 'street_line3', 'city', 'state_province', 'country', 'zip_code', # address info
				'expertise_description', 'notes')
		widgets = {
			'all_types': forms.CheckboxSelectMultiple(),
		}
	def __init__(self, *args, **kwargs):
		super(CompanyRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs = { 'placeholder':'Required' }
		self.fields['region'].empty_label = None
		self.fields['about'].widget.attrs = { 'placeholder':'Optional' }
		self.fields['phone'].widget.attrs = { 'placeholder':'(xxx) xxx-xxxx' }
		self.fields['fax'].widget.attrs = { 'placeholder':'Optional' }
		self.fields['email'].widget.attrs = { 'placeholder':'example@company.com' }
		self.fields['website'].widget.attrs = { 'placeholder':'Optional' }
		self.fields['street_line1'].widget.attrs = { 'placeholder':'Address Line 1' }
		self.fields['street_line2'].widget.attrs = { 'placeholder':'Address Line 2' }
		self.fields['street_line3'].widget.attrs = { 'placeholder':'Address Line 3' }
		self.fields['city'].widget.attrs = { 'placeholder':'City' }
		self.fields['state_province'].widget.attrs = { 'placeholder':'State/Province' }
		self.fields['country'].widget.attrs = { 'placeholder':'Country' }
		self.fields['zip_code'].widget.attrs = { 'placeholder':'Zip #' }
		self.fields['primary_type'].empty_label = None
		self.fields['expertise_description'].widget.attrs = { 'placeholder':'Optional' }
		self.fields['notes'].widget.attrs = { 'placeholder':'Miscellaneous Comments'}
		self.fields['all_types'].required = False

class ContactRegistrationForm(ModelForm):
	# db calls for models
	industry_models = Industry.objects.filter(is_active=True)
	category_models = Category.objects.filter(is_active=True)

	# customized form fields
	industries = forms.ModelMultipleChoiceField(industry_models, widget=forms.CheckboxSelectMultiple(), required=False)
	industry_expertise = forms.ModelMultipleChoiceField(industry_models, widget=forms.CheckboxSelectMultiple(), required=False)
	categories = forms.ModelMultipleChoiceField(category_models, widget=forms.CheckboxSelectMultiple(), required=False)
	category_expertise = forms.ModelMultipleChoiceField(category_models, widget=forms.CheckboxSelectMultiple(), required=False)

	class Meta:
		model = ContactProfile
		# TODO: missing the core expertise fields
		fields = ('first_name', 'last_name', 'department', 'title', 'phone', 'fax', 'email', 'region', 'buy', 'sell', 'primary_type', 'all_types',
				'expertise_description', 'notes')
		widgets = {
			'all_types': forms.CheckboxSelectMultiple(), # preselect
			'buy': forms.RadioSelect,
			'sell': forms.RadioSelect,
		}
	def __init__(self, *args, **kwargs):
		super(ContactRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].widget.attrs = { 'placeholder':'Required' }
		self.fields['last_name'].widget.attrs = { 'placeholder': 'Required' }
		self.fields['department'].widget.attrs = { 'placeholder':'Optional' }
		self.fields['title'].widget.attrs = { 'placeholder':'Optional' }
		self.fields['phone'].widget.attrs = { 'placeholder':'(xxx) xxx-xxxx' }
		self.fields['fax'].widget.attrs = { 'placeholder':'Optional' }
		self.fields['email'].widget.attrs = { 'placeholder':'example@company.com' }
		self.fields['region'].empty_label = None # preselect
		self.fields['buy'].widget.choices = ((False, 'False'), (True, 'True'))
		self.fields['sell'].widget.choices = ((False, 'False'), (True, 'True'))
		self.fields['primary_type'].empty_label = None # preselect
		self.fields['expertise_description'].widget.attrs = { 'placeholder':'Optional' }
		self.fields['notes'].widget.attrs = { 'placeholder':'Optional' }
		self.fields['all_types'].required = False
