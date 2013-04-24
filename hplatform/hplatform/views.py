from django.template import Template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

def home(request):
	return HttpResponse('Welcome to Hyperion!')