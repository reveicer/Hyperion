from django.db import models
from django.contrib.auth.models import User

class TraderProfile(models.Model):
	# access TraderProfile from User via get_profile()
	is_active = models.BooleanField(default=True)
	user = models.ForeignKey(User, unique=True, related_name='TraderProfile')
	first_name = models.CharField('First Name', max_length=50)
	last_name = models.CharField('Last Name', max_length=50)
	title = models.CharField('Title', max_length=20, blank=True)
	phone = models.CharField('Phone', max_length=40)
	fax = models.CharField('Fax', max_length=40, blank=True)

	def __unicode__(self):
		return self.get_full_name()

	def get_full_name(self):        
		return '%s %s' % (self.first_name, self.last_name)