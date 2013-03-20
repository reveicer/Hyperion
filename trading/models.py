from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

'''
industry
'''
class IndustryCategory(models.Model):
	category = models.CharField(_('Catogry'), max_length=50)
	sub_category = models.CharField(_('Sub Catogry'), max_length=50, blank=True)
	
	def __unicode__(self):
		return 'hello'

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
    phone_type = models.CharField(_('Type'), maxlength=10, choices=PHONE_TYPE_CHOICES, default='OTHER')
    number = models.CharField(_('Number'), maxlength=40)
    comment = models.TextField(_('Comment'), blank=True)

    class Meta:
        abstract = True

    def get_concrete_phone(self):
    	if hasattr(self, 'TraderPhone'):
            return self.TraderPhone
        if hasattr(self, 'ContactPhone'):
            return self.ContactPhone

class ContactPhone(AbstractPhone):
	is_active = models.BooleanField(default=False)
    contact = models.ForeignKey(_('Contact'), ContactProfile)

    def __unicode__(self):
    	return '%s: %s' % (self.phone_type, self.number)

class TraderPhone(AbstractPhone):    
    is_active = models.BooleanField(default=False)
    trader = models.ForeignKey(_('Trader'), TraderProfile)

    def __unicode__(self):
		return '%s: %s' % (self.phone_type, self.number)

##########################################################################################
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
    address_type = models.CharField(_('Type'), maxlength=10, choices=ADDRESS_TYPE_CHOICES, default='OTHER')
    street_line1 = models.CharField(_('Address 1'), max_length=100, blank=True)
    street_line2 = models.CharField(_('Address 2'), max_length=100, blank=True)
    city = models.CharField(_('City'), max_length=100, blank=True)
    county = models.CharField(_('County'), max_length=100, blank=True)
    state = models.CharField(_('State'), max_length=100, blank=True)
    province = models.CharField(_('Province'), max_length=100, blank=True)
    country = models.CharField(_('Country'), max_length=100, blank=True)
    zip_code = models.CharField(_('ZIP Code'), max_length=20, blank=True)

    class Meta:
        abstract = True

    def get_concrete_address(self):
    	if hasattr(self, 'CorporateAddress'):
            return self.CorporateAddress
        if hasattr(self, 'ContactAddress'):
            return self.ContactAddress

class CorporateAddress(AbstractAddress):
    is_active = models.BooleanField(default=False)
    corporate = models.ForeignKey(_('Corporate'), CorporateProfile)

    # TODO
	def __unicode__(self):
		return '%s\n%s\n%s\n%s' % (self.street_line1, self.street_line2, self.city, self.country, self.zip_code)

class ContactAddress(AbstractAddress):
    is_active = models.BooleanField(default=False)
    contact = models.ForeignKey(_('Contact'), ContactProfile)

    # TODO
	def __unicode__(self):
		return '%s: %s' % (self.phone_type, self.number)

##########################################################################################
'''
Trader Information
'''
class TraderProfile(models.Model):
	# access TraderProfile from User via get_profile()
	is_active = models.BooleanField(default=False)
	user = models.ForeignKey(User, unique=True)
	title = models.CharField(_('Title'), max_length=20, default='trader')
	expertise = JSONField(_('Expertise'), blank=True, default={})

	def __unicode__(self):
        return self.user.get_full_name()

'''
class models.User
	username 			#Required. 30 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
	first_name 			#Optional. 30 characters or fewer.
	last_name 			#Optional. 30 characters or fewer.
	email 				#Optional. Email address.
	password 			#Required. A hash of, and metadata about, the password. (Django doesn’t store the raw password.) Raw passwords can be arbitrarily long and can contain any character. See the password documentation.
	groups 				#Many-to-many relationship to Group
	user_permissions 	#Many-to-many relationship to Permission
	is_staff 			#Boolean. Designates whether this user can access the admin site.
	is_active 			#Boolean. Designates whether this user account should be considered active. We recommend that you set this flag to False instead of deleting accounts; that way, if your applications have any foreign keys to users, the foreign keys won’t break.
	is_superuser 		#Boolean. Designates that this user has all permissions without explicitly assigning them.
	last_login 			#A datetime of the user’s last login. Is set to the current date/time by default.
	date_joined 		#A datetime designating when the account was created. Is set to the current date/time by default when the account is created.
'''

##########################################################################################
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
		('IRS'. 'Inventory Carrying Reseller'),
		('NIRS', 'Non-inventory Carrying Reseller'),
		('OEM', 'Original Equipment Manufacturer'),
		('SP', 'Service Provider'),
		('RF', 'Refurbisher'),
		('RD', 'R&D'),
		('UNIV', 'University'),
		('OTHER', 'Other'),
	)

	is_active = models.BooleanField(default=False)
	first_name = models.CharField(_('First Name'), max_length=30, blank=True)
	last_name = models.CharField(_('Last Name'), max_length=30, blank=True)
	email = models.EmailField(_('E-mail'), blank=True)
	corporate = models.ForeignKey(_('Employer'), CorporateProfile, blank=True)
	department = models.CharField(_('Department'), max_length=20, blank=True)
	title = models.CharField(_('Title'), max_length=20, blank=True)
	buy = models.BooleanField(_('Buys'), default=False)
	sell = models.BooleanField(_('Sells'), default=False)
	region = models.CharField(_('Region'), max_length=10, choices=REGION_CHOICES, default='OTHER')
	contact_type = models.CharField(_('Type'), max_length=10, choices=CONTACT_TYPE_CHOICES, default='OTHER')
	category = models.ManyToManyField(_('Category'), IndustryCategory)
	expertise = JSONField(_('Expertise'), blank=True, default={})
	notes = models.TextField(_('Notes'), blank=True)

	def get_full_name(self):        
        return '%s %s' % (self.first_name, self.last_name)

	def get_formal_name(self):
        formal_name = '%s, %s' % (self.get_full_name(), self.title)
        return formal_name.strip()

	def __unicode__(self):
		return self.get_full_name()

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
		('IRS'. 'Inventory Carrying Reseller'),
		('NIRS', 'Non-inventory Carrying Reseller'),
		('OEM', 'Original Equipment Manufacturer'),
		('SP', 'Service Provider'),
		('RF', 'Refurbisher'),
		('RD', 'R&D'),
		('UNIV', 'University'),
		('OT', 'Other'),
	)
	is_active = models.BooleanField(default=False)
	name = models.CharField(_('Name'), max_length=50)
	region = models.CharField(_('Region'), max_length=10, choices=REGION_CHOICES, default='OTHER')
	category = models.ManyToManyField(_('Category'), IndustryCategory)
	corporate_type = models.CharField(_('Type'), max_length=10, choices=CORPORATE_TYPE_CHOICES, default='OTHER')
	website = models.URLField(_('Website'), max_length=200)
	description = models.TextField(_('Description'), blank=True)
	notes = models.TextField(_('Notes'), blank=True)

	def __unicode__(self):
		return self.name

##########################################################################################
'''
Equipment Core + Profile
'''
class EquipmentCore(models.Model):
	add_date = models.DateField(_('Date Added'), auto_now_add=True)
	last_modified = models.DateField(_('Last Modified'), auto_now=True, null=True, blank=True)
	make = models.CharField(_('Make'), max_length=50, blank=True)
	model = models.CharField(_('Model'), max_length=50, blank=True)
	year = models.CharField(_('Year'), max_length=4, blank=True)
	price = models.DecimalField(_('Price'), max_digits=15, decimal_places=2, blank=True)
	description = models.TextField(_('Description'), blank=True)

	def __unicode__(self):
		return 'hello' # TODO

class EquipmentProfile(models.Model):
	is_active = models.BooleanField(default=False)
	add_date = models.DateField(_('Date Added'), auto_now_add=True)
	last_modified = models.DateField(_('Last Modified'), auto_now=True, null=True, blank=True)
	core = models.ForeignKey(_('Make & Model'), EquipmentCore)
	serial_number = models.CharField(_('Serial Number'), max_length=100, blank=True)
	category = models.ManyToManyField(_('Category'), IndustryCategory)
	corporate = models.ForeignKey(_('Property of'), CorporateProfile, blank=True)
	contact = models.ForeignKey(_('Contact'), ContactProfile, blank=True) # can only be owned by 1 contact
	manufacture_date = models.DateField(_('Manufacture Date'), auto_now=False, auto_now_add=False, blank=True)
	description = models.TextField(_('Description'), blank=True)
	notes = models.TextField(_('Notes'), blank=True)

	def __unicode__(self):
		return 'hello' # TODO

##########################################################################################
'''
Listings + Requirements
'''
class ListingProfile(models.Model):
	is_active = models.BooleanField(default=False)
	equipment = models.ForeignKey(_('Equipment'), EquipmentProfile)
	price = models.DecimalField(_('Price'), max_digits=15, decimal_places=2)
	post_date = models.DateField(_('Posted on'), auto_now=False, auto_now_add=False, blank=True)
	description = models.TextField(_('Description'), blank=True)

	def __unicode__(self):
		return 'hello' # TODO

class AbstractRequirement(models.Model):
	features = JSONField(_('Feature Requirements'), blank=True, default={})
	price = JSONField(_('Price Requirements'), blank=True, default={}) # TODO: blank JSON Object
	manufacture_date = JSONField(_('Manufacture Date Requirements'), blank=True, default={})	

	class Meta:
        abstract = True

class RequirementProfile(AbstractRequirement):
	is_active = models.BooleanField(default=False)
	contact = models.ForeignKey(_('Posted by'), ContactProfile)
	trader = models.ForeignKey(_('Handled by'), TraderProfile)
	category = models.ManyToManyField(_('Category'), IndustryCategory)
	post_date = models.DateField(_('Posted on'), auto_now_add=True)
	description = models.TextField(_('Description'), blank=True)

	def __unicode__(self):
		return 'hello' # TODO

class RequirementRecommendation(models.Model):
	is_active = models.BooleanField(default=False)
	requirement = models.ForeignKey(_('Requirement'), RequirementProfile)
	core = models.ForeignKey(_('Make & Model'), EquipmentCore)
	trader = models.ForeignKey(_('Proposed by'), TraderProfile)
	notes = models.TextField(_('Notes'), blank=True)

	def __unicode__(self):
		return 'hello' # TODO

##########################################################################################
'''
Transactions
'''
class Transactions(models.Model):
	item = models.ForeignKey(_('Item'), ListingProfile)
	buyer = models.ForeignKey(_('Buyer'), ContactProfile)
	trader = models.ForeignKey(_('Trader'), TraderProfile, blank=True)	
	price = models.DecimalField(_('Price'), max_digits=15, decimal_places=2)
	transaction_date = models.DateField(_('Purchase Date'), auto_now_add=True)
	notes = models.TextField(_('Notes'), blank=True)

	def __unicode__(self):
		return 'hello' # TODO
