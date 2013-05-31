# django imports
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

def home(request):
	template = loader.get_template('home.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))