# import models
from Hyperion.apps.hinventory.models import *

# Django imports
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

#def equipment_profile(request, equipment_id):
#	pass