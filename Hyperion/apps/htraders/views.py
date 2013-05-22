# django imports
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

# models import
from Hyperion.apps.htraders.models import *

# account
import account.views

# import forms
from Hyperion.apps.htraders.forms import *

@login_required
def search(request):
	template = loader.get_template('search.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

#@login_required
class SignupView(account.views.SignupView):
	form_class = SignupForm

	def after_signup(self, form):
		self.create_trader_profile(form)
		super(SignupView, self).after_signup(form)

	def create_trader_profile(self, form):
		profile = TraderProfile(user=self.created_user)
		profile.first_name = form.cleaned_data['first_name']
		profile.last_name = form.cleaned_data['last_name']
		profile.title = form.cleaned_data['title']
		profile.phone = form.cleaned_data['phone']
		profile.fax = form.cleaned_data['fax']
		profile.save()

	def generate_username(self, form):
		username = form.cleaned_data['email']
		return username

class LoginView(account.views.LoginView):
    form_class = LoginEmailForm
    