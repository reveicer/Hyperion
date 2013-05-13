from django.db import models

class Industry(models.Model):
	is_active = models.BooleanField(default=True)
	code = models.CharField('Code', max_length=4)
	name = models.CharField('Name', max_length=50)

	def __unicode__(self):
		return self.name

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
	name = models.CharField('Name', max_length=10)
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
	#categories = models.ManyToManyField(Category, related_name='company_profiles')
	#category_expertise = models.ManyToManyField(Category, related_name='expert_company_profiles')
	#industries = models.ManyToManyField(Industry, related_name='company_profiles')
	#industry_expertise = models.ManyToManyField(Industry, related_name='expert_company_profiles')
	expertise_description = models.TextField('Expertise Description', blank=True)
	core_expertise = models.ManyToManyField('hinventory.EquipmentCore', related_name='expert_company_profiles')
	notes = models.TextField('Notes', blank=True)

	def __unicode__(self):
		return self.name

class ContactProfile(models.Model):
	is_active = models.BooleanField(default=True)
	first_name = models.CharField('First Name', max_length=30, blank=True)
	last_name = models.CharField('Last Name', max_length=30, blank=True)
	company = models.ForeignKey(CompanyProfile, blank=True)
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
	#categories = models.ManyToManyField(Category, related_name='contact_profiles')
	#industry_expertise = models.ManyToManyField(Industry, related_name='expert_contact_profiles')
	#category_expertise = models.ManyToManyField(Category, related_name='expert_contact_profiles')
	expertise_description = models.TextField('Expertise Description', blank=True)
	core_expertise = models.ManyToManyField('hinventory.EquipmentCore', related_name='expert_contact_profiles')
	notes = models.TextField('Notes', blank=True)

	def get_full_name(self):        
		return '%s %s' % (self.first_name, self.last_name)

	def __unicode__(self):
		return self.get_full_name()

class CompanyInIndustry(models.Model):
	is_active = models.BooleanField(default=True)
	company = models.ForeignKey(CompanyProfile)
	industry = models.ForeignKey(Industry)
	expertise = models.BooleanField(default=False)

class CompanyInCategory(models.Model):
	is_active = models.BooleanField(default=True)
	company = models.ForeignKey(CompanyProfile)
	category = models.ForeignKey(Category)
	expertise = models.BooleanField(default=False)

class ContactInIndustry(models.Model):
	is_active = models.BooleanField(default=True)
	contact = models.ForeignKey(ContactProfile)
	industry = models.ForeignKey(Industry)
	expertise = models.BooleanField(default=False)

class ContactInCategory(models.Model):
	is_active = models.BooleanField(default=True)
	contact = models.ForeignKey(ContactProfile)
	category = models.ForeignKey(Category)
	expertise = models.BooleanField(default=False)