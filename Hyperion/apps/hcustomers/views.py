# import models
from Hyperion.apps.hcustomers.models import *

# django imports
from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

# python imports
import sys

class CompanyRegistrationForm(ModelForm):
	# db calls for models
	industry_models = Industry.objects.all()
	category_models = Category.objects.all()

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

def company_profile(request, company_id):
	# TODO: handle 404 page if company is not found.
	# TODO: edit company_profile.html to display model-bounded data
	try: 
		company = CompanyProfile.objects.get(id=company_id, is_active=True)
	except CompanyProfile.DoesNotExist:
		return HttpResponseNotFound('<h1>404: Cannot find company.</h1>') 

	template = loader.get_template('company_profile.html')
	context = RequestContext(request, {
		'company' : company,
		'contact_registration_url': company.get_contact_registration_url(),
	})
	return HttpResponse(template.render(context))

def register_company(request):
	if request.method == 'POST':
		form = CompanyRegistrationForm(request.POST)
		if form.is_valid():
			# saves the company
			new_company = form.save()
			
			# save company_in_industry
			industry_batch = []
			industry_expertise = form.cleaned_data['industry_expertise']
			for industry in form.cleaned_data['industries']:								
				company_in_industry = CompanyInIndustry(company=new_company, industry=industry)
				if industry in industry_expertise:
					company_in_industry.expertise = True
				industry_batch.append(company_in_industry)
			CompanyInIndustry.objects.bulk_create(industry_batch)
			
			# save company_in_category
			category_batch = []
			category_expertise = form.cleaned_data['category_expertise']
			for category in form.cleaned_data['categories']:
				company_in_category = CompanyInCategory(company=new_company, category=category)
				if category in category_expertise:
					company_in_category.expertise = True
				category_batch.append(company_in_category)
			CompanyInCategory.objects.bulk_create(category_batch)

			# redirect to company profile page
			return HttpResponseRedirect('/profile/company/%d/' % new_company.id)
	else:
		form = CompanyRegistrationForm()

	grouped_category_models = Category.objects.get_grouped_categories()
	return render(request, 'company_registration.html', {
		'form' : form,
		'grouped_category_models' : grouped_category_models,
		'post_url': request.get_full_path,
	})


class ContactRegistrationForm(ModelForm):
	# db calls for models
	industry_models = Industry.objects.all()
	category_models = Category.objects.all()

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

def contact_profile(request, contact_id):
	pass

def register_contact(request, company_id):
	try: 
		company = CompanyProfile.objects.get(id=company_id, is_active=True)
	except CompanyProfile.DoesNotExist:
		return HttpResponseNotFound('<h1>404: Cannot find company.</h1>') 

	if request.method == 'POST':
		form = ContactRegistrationForm(request.POST)
		if form.is_valid():
			# saves the contact
			new_contact = form.save()
			
			# save contact_in_industry
			industry_batch = []
			industry_expertise = form.cleaned_data['industry_expertise']
			for industry in form.cleaned_data['industries']:								
				contact_in_industry = ContactInIndustry(contact=new_contact, industry=industry)
				if industry in industry_expertise:
					contact_in_industry.expertise = True
				industry_batch.append(contact_in_industry)
			ContactInIndustry.objects.bulk_create(industry_batch)
			
			# save contact_in_category
			category_batch = []
			category_expertise = form.cleaned_data['category_expertise']
			for category in form.cleaned_data['categories']:
				contact_in_category = ContactInCategory(contact=new_contact, category=category)
				if category in category_expertise:
					contact_in_category.expertise = True
				category_batch.append(contact_in_category)
			ContactInCategory.objects.bulk_create(category_batch)

			# redirect to company profile page
			return HttpResponseRedirect('/profile/contact/%d/' % new_contact.id)
	else:
		form = ContactRegistrationForm()

	grouped_category_models = Category.objects.get_grouped_categories()
	return render(request, 'contact_registration.html', {
		'form' : form,
		'grouped_category_models' : grouped_category_models,
		'company': company,
		'post_url': request.get_full_path,
		'company_profile_url': company.get_profile_url(),
	})