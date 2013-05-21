from django.db import models
from django.contrib.auth.models import User

class TraderProfile(models.Model):
	# access TraderProfile from User via get_profile()
	is_active = models.BooleanField(default=True)
	user = models.ForeignKey(User, unique=True)
	title = models.CharField('Title', max_length=20, blank=True)
	phone = models.CharField('Phone', max_length=40)
	fax = models.CharField('Fax', max_length=40, blank=True)
	#expertise = models.TextField('Expertise', blank=True)

	def __unicode__(self):
		return self.user.get_full_name()