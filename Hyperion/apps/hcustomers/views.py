# import models
from Hyperion.apps.hcustomers.models import *

# import forms
from Hyperion.apps.hcustomers.forms import *

# django imports
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

# python imports
import sys

@login_required
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
		'company_industries': company.get_industries(),
		'company_categories': company.get_grouped_categories(),
		'contacts': company.get_contacts(),
	})
	return HttpResponse(template.render(context))

@login_required
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

	return render(request, 'company_registration.html', {
		'form' : form,
		'grouped_category_models' : Category.objects.get_grouped_categories(),
	})

@login_required
def contact_profile(request, contact_id):
	pass

@login_required
def register_contact(request, company_id):
	try: 
		company = CompanyProfile.objects.get(id=company_id, is_active=True)
	except CompanyProfile.DoesNotExist:
		return HttpResponseNotFound('<h1>404: Cannot find company.</h1>') 

	if request.method == 'POST':
		form = ContactRegistrationForm(request.POST)
		if form.is_valid():
			# saves the contact
			new_contact = form.save(commit=False)
			new_contact.company = company
			new_contact.save()
			form.save_m2m()
			
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
		form = ContactRegistrationForm(initial={
			'region': company.region,
			'primary_type': company.primary_type,
			'all_types': company.get_all_types(),
			'industries': company.get_industries(),
			'industry_expertise': company.get_industry_expertise(),
			'categories': company.get_categories(),
			'category_expertise': company.get_category_expertise(),
		})

	grouped_category_models = Category.objects.get_grouped_categories()
	return render(request, 'contact_registration.html', {
		'form' : form,
		'grouped_category_models' : grouped_category_models,
		'company': company,
	})