from django.db import models

class Industry(models.Model):
	is_active = models.BooleanField(default=False)
	code = models.CharField('Code', max_length=3)
	name = models.CharField('Name', max_length=50)

class Category(models.Model):
	is_active = models.BooleanField(default=False)
	code = models.CharField('Code', max_length=3)
	name = models.CharField('Name', max_length=50)

class SubCategory(models.Model):
	is_active = models.BooleanField(default=False)
	code = models.CharField('Code', max_length=3)
	name = models.CharField('Name', max_length=50)
	category = models.ForeignKey(Category, related_name='subcategories')

class Type(models.Model):
	is_active = models.BooleanField(default=False)
	code = models.CharField('Code', max_length=3)
	name = models.CharField('Name', max_length=50)

class Region(models.Model):
	is_active = models.BooleanField(default=False)
	code = models.CharField('Code', max_length=3)
	name = models.CharField('Name', max_length=50)

class CompanyProfile(models.Model):
	is_active = models.BooleanField(default=False)
	name = models.CharField('Name', max_length=50)
	region = models.ForeignKey(Region)
	primary_type = models.ForeignKey(Type, related_name='primary_company_profiles')
	secondary_types = models.ManyToManyField(Type, related_name='secondary_company_profiles')
	about = models.TextField('About', blank=True)
	categories = models.ManyToManyField(Category, related_name='company_profiles')
	subcategories = models.ManyToManyField(SubCategory, related_name='company_profiles')
	industries = models.ManyToManyField(Industry, related_name='company_profiles')
	website = models.URLField('Website', max_length=200)
	email = models.EmailField('E-mail', blank=True)
	phone = models.CharField('Phone', max_length=40)
	fax = models.CharField('Fax', max_length=40)
	street_line1 = models.CharField('Address 1', max_length=100, blank=True)
	street_line2 = models.CharField('Address 2', max_length=100, blank=True)
	city = models.CharField('City', max_length=100, blank=True)
	county = models.CharField('County', max_length=100, blank=True)
	state = models.CharField('State', max_length=100, blank=True)
	province = models.CharField('Province', max_length=100, blank=True)
	country = models.CharField('Country', max_length=100, blank=True)
	zip_code = models.CharField('ZIP Code', max_length=20, blank=True)
	industry_expertise = models.ManyToManyField(Industry, related_name='expert_company_profiles')
	process_expertise = models.TextField('Process Expertise', blank=True)
	core_expertise = models.ManyToManyField('hinventory.EquipmentCore', related_name='expert_company_profiles')
	notes = models.TextField('Notes', blank=True)

	def __unicode__(self):
		return self.name

class ContactProfile(models.Model):
	is_active = models.BooleanField(default=False)
	first_name = models.CharField('First Name', max_length=30, blank=True)
	last_name = models.CharField('Last Name', max_length=30, blank=True)
	region = models.ForeignKey(Region, related_name='contact_profiles')
	primary_type = models.ForeignKey(Type, related_name='primary_contact_profiles')
	secondary_types = models.ManyToManyField(Type, related_name='secondary_contact_profiles')
	categories = models.ManyToManyField(Category, related_name='contact_profiles')
	subcategories = models.ManyToManyField(SubCategory, related_name='contact_profiles')
	email = models.EmailField('E-mail', blank=True)
	company = models.ForeignKey(CompanyProfile, blank=True)
	department = models.CharField('Department', max_length=20, blank=True)
	title = models.CharField('Title', max_length=20, blank=True)
	buy = models.BooleanField('Buys', default=False)
	sell = models.BooleanField('Sells', default=False)
	industry_expertise = models.ManyToManyField(Industry, related_name='expert_contact_profiles')
	process_expertise = models.TextField('Process Expertise', blank=True)
	core_expertise = models.ManyToManyField('hinventory.EquipmentCore', related_name='expert_contact_profiles')
	notes = models.TextField('Notes', blank=True)

	def get_full_name(self):        
		return '%s %s' % (self.first_name, self.last_name)

	def __unicode__(self):
		return self.get_full_name()

class ContactPhone(models.Model):
	PHONE_TYPE_CHOICES = (
		('HOME', 'Home'),
		('WORK', 'Work'),
		('MOBILE', 'Mobile'),
		('FAX', 'Fax'),
		('OTHER', 'Other'),
	)

	is_active = models.BooleanField(default=False)
	contact = models.ForeignKey(ContactProfile, related_name='contact_phones')
	phone_type = models.CharField('Type', max_length=10, choices=PHONE_TYPE_CHOICES, default='OTHER')
	number = models.CharField('Number', max_length=40)
	comment = models.TextField('Comment', blank=True)

class ContactAddress(models.Model):
	ADDRESS_TYPE_CHOICES = (
		('CORP', 'Corporate'),
		('MAIL', 'Mailing'),
		('WORK', 'Work'),
		('OTHER', 'Other'),
	)

	is_active = models.BooleanField(default=False)
	contact = models.ForeignKey(ContactProfile, related_name='contact_addresses')
	address_type = models.CharField('Type', max_length=10, choices=ADDRESS_TYPE_CHOICES, default='OTHER')
	street_line1 = models.CharField('Address 1', max_length=100, blank=True)
	street_line2 = models.CharField('Address 2', max_length=100, blank=True)
	city = models.CharField('City', max_length=100, blank=True)
	county = models.CharField('County', max_length=100, blank=True)
	state = models.CharField('State', max_length=100, blank=True)
	province = models.CharField('Province', max_length=100, blank=True)
	country = models.CharField('Country', max_length=100, blank=True)
	zip_code = models.CharField('ZIP Code', max_length=20, blank=True)