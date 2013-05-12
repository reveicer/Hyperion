from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

#@login_required
def dashboard(request, trader_id):
	t = loader.get_template('dashboard.html')
	return HttpResponse(t.render(Context()))
