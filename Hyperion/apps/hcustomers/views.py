# import models
from Hyperion.apps.hcustomers.models import *

# django imports
from django.forms import ModelForm
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

def company_profile(request, company_id):
	#u = request.user
	t = loader.get_template('company_profile.html')
	return HttpResponse(t.render(Context()))

#def contact_profile(request, contact_id):

class CompanyRegistrationForm(ModelForm):
	# overriding labels
	#name = TextField(label='Company Name')

	class Meta:
		model = CompanyProfile
		# missing the three expertise fields
		fields = ('name', 'phone', 'fax', 'email', 'website', 'region', 'primary_type', 'secondary_types', 'about',
				'street_line1', 'street_line2', 'street_line3', 'city', 'county', 'state', 'province', 'country', 'zip_code', # address info
				'categories', 'subcategories', 'industries', 'expertise_description', 'notes')
		#widgets = {
		#	'name': Textarea(attrs={'cols': 80, 'rows': 20}),
		#}

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

	return render(request, 'company_registration.html', {
			'form' : form,
		})

#def register_contact(request):