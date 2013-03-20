from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

##########################################################################################
'''
industry
'''
class IndustryCategory(models.Model):
	category = models.CharField('Catogry', max_length=50)
	sub_category = models.CharField('Sub Catogry', max_length=50, blank=True)
	
	def __unicode__(self):
		return 'hello'

##########################################################################################
'''
Trader Information
'''
class TraderProfile(models.Model):
	# access TraderProfile from User via get_profile()
	is_active = models.BooleanField(default=False)
	user = models.ForeignKey(User, unique=True)
	title = models.CharField('Title', max_length=20, default='trader')
	expertise = JSONField('Expertise', blank=True, default={})

	def __unicode__(self):
		return self.user.get_full_name()

##########################################################################################
'''
Corporate Information
'''
class CorporateProfile(models.Model):
	REGION_CHOICES = (
		('AS', 'Asia'),
		('EU', 'Europe'),
		('NA', 'North America'),
		('LA', 'Latin America'),
		('OT', 'Other'),
	)
	CORPORATE_TYPE_CHOICES = (
		('EU', 'End User'),
		('IRS', 'Inventory Carrying Reseller'),
		('NIRS', 'Non-inventory Carrying Reseller'),
		('OEM', 'Original Equipment Manufacturer'),
		('SP', 'Service Provider'),
		('RF', 'Refurbisher'),
		('RD', 'R&D'),
		('UNIV', 'University'),
		('OT', 'Other'),
	)
	is_active = models.BooleanField(default=False)
	name = models.CharField('Name', max_length=50)
	region = models.CharField('Region', max_length=10, choices=REGION_CHOICES, default='OTHER')
	category = models.ManyToManyField(IndustryCategory)
	corporate_type = models.CharField('Type', max_length=10, choices=CORPORATE_TYPE_CHOICES, default='OTHER')
	website = models.URLField('Website', max_length=200)
	description = models.TextField('Description', blank=True)
	notes = models.TextField('Notes', blank=True)

	def __unicode__(self):
		return self.name

'''
Contact Information
'''
class ContactProfile(models.Model):
	REGION_CHOICES = (
		('ASIA', 'Asia'),
		('EUROPE', 'Europe'),
		('NAMERICA', 'North America'),
		('LAMERICA', 'Latin America'),
		('OTHER', 'Other'),
	)
	CONTACT_TYPE_CHOICES = (
		('EU', 'End User'),
		('IRS', 'Inventory Carrying Reseller'),
		('NIRS', 'Non-inventory Carrying Reseller'),
		('OEM', 'Original Equipment Manufacturer'),
		('SP', 'Service Provider'),
		('RF', 'Refurbisher'),
		('RD', 'R&D'),
		('UNIV', 'University'),
		('OTHER', 'Other'),
	)

	is_active = models.BooleanField(default=False)
	first_name = models.CharField('First Name', max_length=30, blank=True)
	last_name = models.CharField('Last Name', max_length=30, blank=True)
	email = models.EmailField('E-mail', blank=True)
	corporate = models.ForeignKey(CorporateProfile, blank=True, verbose_name='Employer')
	department = models.CharField('Department', max_length=20, blank=True)
	title = models.CharField('Title', max_length=20, blank=True)
	buy = models.BooleanField('Buys', default=False)
	sell = models.BooleanField('Sells', default=False)
	region = models.CharField('Region', max_length=10, choices=REGION_CHOICES, default='OTHER')
	contact_type = models.CharField('Type', max_length=10, choices=CONTACT_TYPE_CHOICES, default='OTHER')
	category = models.ManyToManyField(IndustryCategory)
	expertise = JSONField('Expertise', blank=True, default={})
	notes = models.TextField('Notes', blank=True)

	def get_full_name(self):        
		return '%s %s' % (self.first_name, self.last_name)

	def get_formal_name(self):
		formal_name = '%s, %s' % (self.get_full_name(), self.title)
		return formal_name.strip()

	def __unicode__(self):
		return self.get_full_name()

##########################################################################################
'''
Phone
'''
class AbstractPhone(models.Model):
	PHONE_TYPE_CHOICES = (
		('HOME', 'Home'),
		('WORK', 'Work'),
		('MOBILE', 'Mobile'),
		('FAX', 'Fax'),
		('OTHER', 'Other'),
	)
	phone_type = models.CharField('Type', max_length=10, choices=PHONE_TYPE_CHOICES, default='OTHER')
	number = models.CharField('Number', max_length=40)
	comment = models.TextField('Comment', blank=True)

	class Meta:
		abstract = True

	def get_concrete_phone(self):
		if hasattr(self, 'TraderPhone'):
			return self.TraderPhone
		if hasattr(self, 'ContactPhone'):
			return self.ContactPhone

class ContactPhone(AbstractPhone):
	is_active = models.BooleanField(default=False)
	contact = models.ForeignKey(ContactProfile, verbose_name='Contact')

	def __unicode__(self):
		return '%s: %s' % (self.phone_type, self.number)

class TraderPhone(AbstractPhone):    
	is_active = models.BooleanField(default=False)
	trader = models.ForeignKey(TraderProfile, verbose_name='Trader')

	def __unicode__(self):
		return '%s: %s' % (self.phone_type, self.number)

'''
Address
'''
class AbstractAddress(models.Model):
	ADDRESS_TYPE_CHOICES = (
		('CORP', 'Corporate'),
		('MAIL', 'Mailing'),
		('WORK', 'Work'),
		('OTHER', 'Other'),
	)
	address_type = models.CharField('Type', max_length=10, choices=ADDRESS_TYPE_CHOICES, default='OTHER')
	street_line1 = models.CharField('Address 1', max_length=100, blank=True)
	street_line2 = models.CharField('Address 2', max_length=100, blank=True)
	city = models.CharField('City', max_length=100, blank=True)
	county = models.CharField('County', max_length=100, blank=True)
	state = models.CharField('State', max_length=100, blank=True)
	province = models.CharField('Province', max_length=100, blank=True)
	country = models.CharField('Country', max_length=100, blank=True)
	zip_code = models.CharField('ZIP Code', max_length=20, blank=True)

	class Meta:
		abstract = True

	def get_concrete_address(self):
		if hasattr(self, 'CorporateAddress'):
			return self.CorporateAddress
		if hasattr(self, 'ContactAddress'):
			return self.ContactAddress

class CorporateAddress(AbstractAddress):
	is_active = models.BooleanField(default=False)
	corporate = models.ForeignKey(CorporateProfile, verbose_name='Corporate')

	# TODO
	def __unicode__(self):
		return '%s\n%s\n%s\n%s' % (self.street_line1, self.street_line2, self.city, self.country, self.zip_code)

class ContactAddress(AbstractAddress):
	is_active = models.BooleanField(default=False)
	contact = models.ForeignKey(ContactProfile, verbose_name='Contact')

	# TODO
	def __unicode__(self):
		return '%s: %s' % (self.phone_type, self.number)

##########################################################################################
'''
Equipment Core + Profile
'''
class EquipmentCore(models.Model):
	add_date = models.DateField('Date Added', auto_now_add=True)
	last_modified = models.DateField('Last Modified', auto_now=True, null=True, blank=True)
	make = models.CharField('Make', max_length=50, blank=True)
	model = models.CharField('Model', max_length=50, blank=True)
	year = models.CharField('Year', max_length=4, blank=True)
	price = models.DecimalField('Price', max_digits=15, decimal_places=2, blank=True)
	description = models.TextField('Description', blank=True)

	def __unicode__(self):
		return 'hello' # TODO

class EquipmentProfile(models.Model):
	is_active = models.BooleanField(default=False)
	add_date = models.DateField('Date Added', auto_now_add=True)
	last_modified = models.DateField('Last Modified', auto_now=True, null=True, blank=True)
	core = models.ForeignKey(EquipmentCore, verbose_name='Make & Model')
	serial_number = models.CharField('Serial Number', max_length=100, blank=True)
	category = models.ManyToManyField(IndustryCategory)
	corporate = models.ForeignKey(CorporateProfile, blank=True, verbose_name='Property of')
	contact = models.ForeignKey(ContactProfile, blank=True, verbose_name='Contact') # can only be owned by 1 contact
	manufacture_date = models.DateField('Manufacture Date', auto_now=False, auto_now_add=False, blank=True)
	description = models.TextField('Description', blank=True)
	notes = models.TextField('Notes', blank=True)

	def __unicode__(self):
		return 'hello' # TODO

##########################################################################################
'''
Listings + Requirements
'''
class ListingProfile(models.Model):
	is_active = models.BooleanField(default=False)
	equipment = models.ForeignKey(EquipmentProfile, verbose_name='Equipment')
	price = models.DecimalField('Price', max_digits=15, decimal_places=2)
	post_date = models.DateField('Posted on', auto_now=False, auto_now_add=False, blank=True)
	description = models.TextField('Description', blank=True)

	def __unicode__(self):
		return 'hello' # TODO

class AbstractRequirement(models.Model):
	features = JSONField('Feature Requirements', blank=True, default={})
	price = JSONField('Price Requirements', blank=True, default={}) # TODO: blank JSON Object
	manufacture_date = JSONField('Manufacture Date Requirements', blank=True, default={})	

	class Meta:
		abstract = True

class RequirementProfile(AbstractRequirement):
	is_active = models.BooleanField(default=False)
	contact = models.ForeignKey(ContactProfile, verbose_name='Posted by')
	trader = models.ForeignKey(TraderProfile, verbose_name='Handled by')
	category = models.ManyToManyField(IndustryCategory)
	post_date = models.DateField('Posted on', auto_now_add=True)
	description = models.TextField('Description', blank=True)

	def __unicode__(self):
		return 'hello' # TODO

class RequirementRecommendation(models.Model):
	is_active = models.BooleanField(default=False)
	requirement = models.ForeignKey(RequirementProfile, verbose_name='Requirement')
	core = models.ForeignKey(EquipmentCore, verbose_name='Make & Model')
	trader = models.ForeignKey(TraderProfile, verbose_name='Proposed by')
	notes = models.TextField('Notes', blank=True)

	def __unicode__(self):
		return 'hello' # TODO

##########################################################################################
'''
Transactions
'''
class Transactions(models.Model):
	item = models.ForeignKey(ListingProfile, verbose_name='Item')
	buyer = models.ForeignKey(ContactProfile, verbose_name='Buyer')
	trader = models.ForeignKey(TraderProfile, blank=True, verbose_name='Trader')
	price = models.DecimalField('Price', max_digits=15, decimal_places=2)
	transaction_date = models.DateField('Purchase Date', auto_now_add=True)
	notes = models.TextField('Notes', blank=True)

	def __unicode__(self):
		return 'hello' # TODO
