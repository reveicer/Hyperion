from django.db import models
from django.contrib.auth.models import User

class TraderProfile(models.Model):
	# access TraderProfile from User via get_profile()
	is_active = models.BooleanField(default=True)
	user = models.ForeignKey(User, unique=True)
	title = models.CharField('Title', max_length=20)
	#expertise = models.TextField('Expertise', blank=True)

	def __unicode__(self):
		return self.user.get_full_name()

class TraderPhone(models.Model):
	PHONE_TYPE_CHOICES = (
		('HOME', 'Home'),
		('WORK', 'Work'),
		('MOBILE', 'Mobile'),
		('FAX', 'Fax'),
		('OTHER', 'Other'),
	)

	is_active = models.BooleanField(default=True)
	phone_type = models.CharField('Type', max_length=10, choices=PHONE_TYPE_CHOICES, default='OTHER')
	number = models.CharField('Number', max_length=40)
	comment = models.TextField('Comment', blank=True)
	trader = models.ForeignKey(TraderProfile)

	def __unicode__(self):
		return '%s: %s' % (self.phone_type, self.number)