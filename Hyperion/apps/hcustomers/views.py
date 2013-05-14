# import models
from Hyperion.apps.hcustomers.models import *

# django imports
from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

# python imports
import sys

class CompanyRegistrationForm(ModelForm):
	# db calls for models
	industry_models = Industry.objects.all()

	# customized form fields
	industries = forms.ModelMultipleChoiceField(industry_models, widget=forms.CheckboxSelectMultiple(), required=False)
	industry_expertise = forms.ModelMultipleChoiceField(industry_models, widget=forms.CheckboxSelectMultiple(), required=False)

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
		self.fields['notes'].widget.attrs = { 'placeholder':'Miscellaneous Comments'}

def company_profile(request, company_id):
	# TODO: handle 404 page if company is not found.
	# TODO: edit company_profile.html to display model-bounded data
	company = CompanyProfile.objects.get(id=company_id)

	template = loader.get_template('company_profile.html')
	context = RequestContext(request, {
		'company' : company,	
	})
	return HttpResponse(template.render(context))

def register_company(request):
	if request.method == 'POST':
		form = CompanyRegistrationForm(request.POST)
		if form.is_valid():
			#print >> sys.stderr, ":: %s" % form.cleaned_data['name']
			#for ie in form.cleaned_data['industry_expertise']:
			#	print >> sys.stderr, ':: %s' % ie

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


			# redirect to company profile page
			return HttpResponseRedirect('/profile/company/%d/' % new_company.id)
	else:
		form = CompanyRegistrationForm()

	grouped_categories = Category.objects.get_grouped_categories()
	return render(request, 'company_registration.html', {
			'form' : form,
			'grouped_categories' : grouped_categories,
		})

#def register_contact(request):