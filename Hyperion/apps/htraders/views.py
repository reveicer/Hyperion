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

#@login_required
def dashboard(request):
	t = loader.get_template('dashboard.html')
	return HttpResponse(t.render(Context()))

class SignupView(account.views.SignupView):
	form_class = SignupForm

	def after_signup(self, form):
		self.create_trader_profile(form)
		super(SignupView, self).after_signup(form)

	def create_trader_profile(self, form):
		profile = TraderProfile(user=self.created_user)
		profile.title = form.cleaned_data['title']
		profile.phone = form.cleaned_data['phone']
		profile.fax = form.cleaned_data['fax']
		profile.save()

	def generate_username(self, form):
		username = form.cleaned_data['email']
		return username

class LoginView(account.views.LoginView):
    form_class = account.forms.LoginEmailForm
    