from django.db import models
from Hyperion.apps.htraders.models import TraderProfile

# python imports
import json, datetime

class CategoryManager(models.Manager):
	def get_grouped_categories(self):
		grouped_dict = {}

		active_categories = self.filter(is_active=True)
		for active_category in active_categories:
			category_name = active_category.category_name
			existing_list = grouped_dict.get(category_name)

			if existing_list is None:
				grouped_dict[category_name] = [active_category]
			else:
				existing_list.append(active_category)
				grouped_dict[category_name] = existing_list

		return grouped_dict

class CompanyInIndustryManager(models.Manager):
	def get_industries(self, company):
		return Industry.objects.filter(companies_in_industry__is_active=True, companies_in_industry__company=company)

	def get_industries_of_expertise(self, company):
		return Industry.objects.filter(companies_in_industry__is_active=True, companies_in_industry__company=company, companies_in_industry__expertise=True)		

class ContactInIndustryManager(models.Manager):
	def get_industries(self, contact):
		return Industry.objects.filter(contacts_in_industry__is_active=True, contacts_in_industry__contact=contact)

	def get_industries_of_expertise(self, contact):
		return Industry.objects.filter(contacts_in_industry__is_active=True, contacts_in_industry__contact=contact, contacts_in_industry__expertise=True)		

class CompanyInCategoryManager(models.Manager):
	def get_categories(self, company):
		return Category.objects.filter(companies_in_category__is_active=True, companies_in_category__company=company)

	def get_categories_of_expertise(self, company):
		return Category.objects.filter(companies_in_category__is_active=True, companies_in_category__company=company, companies_in_category__expertise=True)

	def get_grouped_categories(self, company):
		grouped_dict = {}

		active_company_categories = self.filter(is_active=True, company=company)
		for active_company_category in active_company_categories:
			category = active_company_category.category
			category_name = category.category_name
			existing_list = grouped_dict.get(category_name)

			if existing_list is None:
				grouped_dict[category_name] = [category]
			else:
				existing_list.append(category)
				grouped_dict[category_name] = existing_list

		return grouped_dict

class ContactInCategoryManager(models.Manager):
	def get_categories(self, contact):
		return Category.objects.filter(contacts_in_category__is_active=True, contacts_in_category__contact=contact)

	def get_categories_of_expertise(self, contact):
		return Category.objects.filter(contacts_in_category__is_active=True, contacts_in_category__contact=contact, contacts_in_category__expertise=True)

	def get_grouped_categories(self, contact):
		grouped_dict = {}

		active_contact_categories = self.filter(is_active=True, contact=contact)
		for active_contact_category in active_contact_categories:
			category = active_contact_category.category
			category_name = category.category_name
			existing_list = grouped_dict.get(category_name)

			if existing_list is None:
				grouped_dict[category_name] = [category]
			else:
				existing_list.append(category)
				grouped_dict[category_name] = existing_list

		return grouped_dict

class Industry(models.Model):
	is_active = models.BooleanField(default=True)
	code = models.CharField('Code', max_length=4)
	name = models.CharField('Name', max_length=50)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['id']

class Category(models.Model):
	is_active = models.BooleanField(default=True)
	category_code = models.CharField('Category Code', max_length=4)
	category_name = models.CharField('Category Name', max_length=50)
	subcategory_code = models.CharField('SubCategory Code', max_length=4)
	subcategory_name = models.CharField('SubCategory Name', max_length=50)
	# custom manager
	objects = CategoryManager()

	def __unicode__(self):
		return self.subcategory_name
		
	class Meta:
		ordering = ['category_name', 'subcategory_name']

class Type(models.Model):
	is_active = models.BooleanField(default=True)
	code = models.CharField('Code', max_length=4)
	name = models.CharField('Name', max_length=50)

	def __unicode__(self):
		return self.name

class Region(models.Model):
	is_active = models.BooleanField(default=True)
	code = models.CharField('Code', max_length=4)
	name = models.CharField('Name', max_length=50)

	def __unicode__(self):
		return self.name

class CompanyProfile(models.Model):
	is_active = models.BooleanField(default=True)
	name = models.CharField('Name', max_length=100)
	phone = models.CharField('Phone', max_length=40)
	fax = models.CharField('Fax', max_length=40, blank=True)
	email = models.EmailField('E-mail', blank=True)
	website = models.URLField('Website', max_length=200, blank=True)
	region = models.ForeignKey(Region)
	primary_type = models.ForeignKey(Type, related_name='primary_company_profiles')
	all_types = models.ManyToManyField(Type, related_name='all_company_profiles')
	about = models.TextField('About', blank=True)
	street_line1 = models.CharField('Address 1', max_length=100, blank=True)
	street_line2 = models.CharField('Address 2', max_length=100, blank=True)
	street_line3 = models.CharField('Address 3', max_length=100, blank=True)
	city = models.CharField('City', max_length=100, blank=True)
	state_province = models.CharField('State/Province', max_length=100, blank=True)
	country = models.CharField('Country', max_length=100, blank=True)
	zip_code = models.CharField('ZIP Code', max_length=20, blank=True)
	expertise_description = models.TextField('Expertise Description', blank=True)
	core_expertise = models.ManyToManyField('hinventory.EquipmentCore', related_name='expert_company_profiles')
	notes = models.TextField('Notes', blank=True)

	def __unicode__(self):
		return self.name

	def get_profile_url(self):
		return '/profile/company/%d/' % self.id

	def get_contact_registration_url(self):
		return '/profile/register/contact/%d/' % self.id

	def get_contact_count(self):
		return len(self.contacts.filter(is_active=True))

	def get_contacts(self):
		return self.contacts.filter(is_active=True)

	def get_all_types(self):
		return self.all_types.filter(is_active=True)

	def get_industries(self):
		return CompanyInIndustry.objects.get_industries(self)

	def get_industry_expertise(self):
		return CompanyInIndustry.objects.get_industries_of_expertise(self)

	def get_categories(self):
		return CompanyInCategory.objects.get_categories(self)

	def get_category_expertise(self):
		return CompanyInCategory.objects.get_categories_of_expertise(self)

	def get_grouped_categories(self):
		return CompanyInCategory.objects.get_grouped_categories(self)

	def to_dict(self):
		dict_response = {}
		dict_response['id'] = self.id
		dict_response['name'] = self.name
		dict_response['phone'] = self.phone
		dict_response['email'] = self.email
		return dict_response

class ContactProfile(models.Model):
	is_active = models.BooleanField(default=True)
	first_name = models.CharField('First Name', max_length=30, blank=True)
	last_name = models.CharField('Last Name', max_length=30, blank=True)
	company = models.ForeignKey(CompanyProfile, blank=True, related_name='contacts')
	department = models.CharField('Department', max_length=20, blank=True)
	title = models.CharField('Title', max_length=20, blank=True)
	phone = models.CharField('Phone', max_length=40)
	fax = models.CharField('Fax', max_length=40, blank=True)
	email = models.EmailField('E-mail', blank=True)
	region = models.ForeignKey(Region, related_name='contact_profiles')
	buy = models.BooleanField('Buys', default=False)
	sell = models.BooleanField('Sells', default=False)
	primary_type = models.ForeignKey(Type, related_name='primary_contact_profiles')
	all_types = models.ManyToManyField(Type, related_name='all_contact_profiles')
	expertise_description = models.TextField('Expertise Description', blank=True)
	core_expertise = models.ManyToManyField('hinventory.EquipmentCore', related_name='expert_contact_profiles')
	notes = models.TextField('Notes', blank=True)

	def __unicode__(self):
		return self.get_full_name()

	def get_full_name(self):        
		return '%s %s' % (self.first_name, self.last_name)

	def get_industries(self):
		return ContactInIndustry.objects.get_industries(self)

	def get_grouped_categories(self):
		return ContactInCategory.objects.get_grouped_categories(self)

	def get_correspondences(self):
		return Correspondence.objects.filter(is_active=True, contact=self)

class CompanyInIndustry(models.Model):
	is_active = models.BooleanField(default=True)
	company = models.ForeignKey(CompanyProfile, related_name='industries')
	industry = models.ForeignKey(Industry, related_name='companies_in_industry')
	expertise = models.BooleanField(default=False)
	objects = CompanyInIndustryManager()

	class Meta:
		ordering = ['company', 'expertise']

class CompanyInCategory(models.Model):
	is_active = models.BooleanField(default=True)
	company = models.ForeignKey(CompanyProfile, related_name='categories')
	category = models.ForeignKey(Category, related_name='companies_in_category')
	expertise = models.BooleanField(default=False)
	objects = CompanyInCategoryManager()

	class Meta:
		ordering = ['company', 'expertise']

class ContactInIndustry(models.Model):
	is_active = models.BooleanField(default=True)
	contact = models.ForeignKey(ContactProfile)
	industry = models.ForeignKey(Industry, related_name='contacts_in_industry')
	expertise = models.BooleanField(default=False)
	objects = ContactInIndustryManager()

	class Meta:
		ordering = ['contact', 'expertise']

class ContactInCategory(models.Model):
	is_active = models.BooleanField(default=True)
	contact = models.ForeignKey(ContactProfile)
	category = models.ForeignKey(Category, related_name='contacts_in_category')
	expertise = models.BooleanField(default=False)
	objects = ContactInCategoryManager()

	class Meta:
		ordering = ['contact', 'expertise']

class Correspondence(models.Model):
	is_active = models.BooleanField(default=True)
	contact = models.ForeignKey(ContactProfile)
	trader = models.ForeignKey(TraderProfile)
	message = models.TextField(blank=False)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['contact', '-timestamp']

	def get_timestamp(self):
		return self.timestamp.strftime("%Y-%m-%d %H:%M")

	def to_json(self):
		json_response = {}
		json_response['contact'] = self.contact.get_full_name()
		json_response['trader'] = self.trader.get_full_name()
		json_response['message'] = self.message
		json_response['timestamp'] = self.get_timestamp()
		return json.dumps(json_response)