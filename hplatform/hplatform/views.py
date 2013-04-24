from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

def home(request):
	t = loader.get_template('home.html')
	return HttpResponse(t.render(Context()))