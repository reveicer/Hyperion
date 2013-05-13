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

def company_profile(request, company_id):
	#u = request.user
	t = loader.get_template('company_profile.html')
	return HttpResponse(t.render(Context()))

class CompanyRegistrationForm(ModelForm):
	industries = forms.ModelMultipleChoiceField(Industry.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)

	class Meta:
		model = CompanyProfile
		# missing the three expertise fields
		fields = ('name', 'phone', 'fax', 'email', 'website', 'region', 'primary_type', 'all_types', 'about',
				'street_line1', 'street_line2', 'street_line3', 'city', 'state_province', 'country', 'zip_code', # address info
				'categories', 'expertise_description', 'notes')
		widgets = {
			# uncomment this if reading fails.
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

def register_company(request):
	if request.method == 'POST':
		form = CompanyRegistrationForm(request.POST)
		if form.is_valid():
			company = form.save(commit=False)
			# do something else
			company.is_active = True
			company.save()
			form.save_m2m()

			# redirect to company profile page
			return HttpResponseRedirect('/profile/company/' + company.id + '/')
	else:
		form = CompanyRegistrationForm()


	grouped_categories = Category.objects.get_grouped_categories()
	return render(request, 'company_registration.html', {
			'form' : form,
			'grouped_categories' : grouped_categories,
		})

#def register_contact(request):