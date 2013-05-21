# models import
from Hyperion.apps.htraders.models import *

# django imports
from django import forms

# account
import account.forms

class SignupForm(account.forms.SignupForm):
	title = forms.CharField(
		max_length=TraderProfile._meta.get_field('title').max_length, 
		required=not TraderProfile._meta.get_field('title').blank)
	phone = forms.CharField(
		max_length=TraderProfile._meta.get_field('phone').max_length, 
		required=not TraderProfile._meta.get_field('phone').blank)
	fax = forms.CharField(
		max_length=TraderProfile._meta.get_field('fax').max_length, 
		required=not TraderProfile._meta.get_field('fax').blank)

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		del self.fields['username']
		self.fields['email'].widget.attrs = { 'placeholder':'trader@hyperionmarkets.net' }
		self.fields['password'].widget.attrs = { 'placeholder':'password' }
		self.fields['password_confirm'].widget.attrs = { 'placeholder':'password again' }
		self.fields['title'].widget.attrs = { 'placeholder':'Optional' }
		self.fields['phone'].widget.attrs = { 'placeholder':'(xxx) xxx-xxxx' }
		self.fields['fax'].widget.attrs = { 'placeholder':'Optional' }
