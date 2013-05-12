# import models
from Hyperion.apps.hcustomers.models import *

# django imports
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

def company_profile(request, company_id):
	#u = request.user
	t = loader.get_template('company_profile.html')
	return HttpResponse(t.render(Context()))

#def contact_profile(request, contact_id):

def register_company(request):
	#if request.method == 

#def register_contact(request):