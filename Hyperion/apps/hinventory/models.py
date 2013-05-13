from django.db import models
from Hyperion.apps.htraders.models import TraderProfile
from Hyperion.apps.hcustomers.models import CompanyProfile, ContactProfile, Category
	
class EquipmentCore(models.Model):
	is_active = models.BooleanField(default=True)
	make = models.CharField('Make', max_length=50, blank=True)
	model = models.CharField('Model', max_length=50, blank=True)
	year = models.CharField('Year', max_length=4, blank=True)
	categories = models.ManyToManyField(Category, related_name='equipment_cores')
	about = models.TextField('About', blank=True)

class EquipmentCorePrice(models.Model):
	is_active = models.BooleanField(default=True)
	core = models.ForeignKey(EquipmentCore, related_name='equipment_core_prices')
	price = models.DecimalField('Price', max_digits=15, decimal_places=2)
	date_recorded = models.DateField('Date Recorded', auto_now_add=True)
	notes = models.TextField('Notes', blank=True)

class EquipmentProfile(models.Model):
	is_active = models.BooleanField(default=True)
	date_created = models.DateField('Date Created', auto_now_add=True)
	core = models.ForeignKey(EquipmentCore, related_name='equipment_profiles')
	serial_number = models.CharField('Serial Number', max_length=100, blank=True, null=True)
	date_manufactured = models.DateField('Manufacture Date', blank=True)
	about =  models.TextField('About', blank=True)
	company = models.ForeignKey(CompanyProfile, related_name='equipment_profiles')
	primary_contact = models.ForeignKey(ContactProfile, related_name='primary_equipment_profiles')
	secondary_contacts = models.ManyToManyField(ContactProfile, related_name='secondary_equipment_profiles')
	notes = models.TextField('Notes', blank=True)

class EquipmentProfileUpdate(models.Model):
	original_equipment = models.ForeignKey(EquipmentProfile, related_name='equipment_profile_update_from')
	updated_equipment = models.ForeignKey(EquipmentProfile, related_name='equipment_profile_update_to')
	date_updated = models.DateField('Date Updated', auto_now_add=True)
	trader = models.ForeignKey(TraderProfile, related_name='equipment_profile_updates')
	notes = models.TextField('Notes', blank=True)

class ListingProfile(models.Model):
	is_active = models.BooleanField(default=True)
	equipment = models.ForeignKey(EquipmentProfile, related_name='listing_profiles')
	seller = models.ForeignKey(ContactProfile, related_name='listing_profiles')
	price = models.DecimalField('Price', max_digits=15, decimal_places=2)
	date_posted = models.DateField('Date Posted', auto_now_add=True)
	notes = models.TextField('Notes', blank=True)
	
class Transaction(models.Model):
	equipment = models.ForeignKey(ListingProfile, related_name='transactions')
	buyer_company = models.ForeignKey(CompanyProfile, related_name='transactions')
	buyer_contact = models.ForeignKey(ContactProfile, related_name='transactions')
	primary_trader = models.ForeignKey(TraderProfile, related_name='primary_transactions')
	secondary_traders = models.ManyToManyField(TraderProfile, related_name='secondary_transactions')
	price = models.DecimalField('Price', max_digits=15, decimal_places=2)
	date_purchased = models.DateField('Date Purchased', auto_now_add=True)
	notes = models.TextField('Notes', blank=True)

class RequirementProfile(models.Model):
	is_active = models.BooleanField(default=True)
	description = models.TextField('Description', blank=True)
	max_price = models.DecimalField('Max Price', max_digits=15, decimal_places=2)
	min_price = models.DecimalField('Min Price', max_digits=15, decimal_places=2)
	expected_price = models.DecimalField('Expected Price', max_digits=15, decimal_places=2, blank=True)
	earliest_manufacture_year = models.CharField('Manufactured After', max_length=4, blank=True)
	latest_manufacture_year = models.CharField('Manufactured Before', max_length=4, blank=True)
	expected_manufacture_year = models.CharField('Expected Manufacture Year', max_length=4, blank=True)
	company = models.ForeignKey(CompanyProfile, related_name='requirement_profiles')
	contact = models.ForeignKey(ContactProfile, related_name='requirement_profiles')
	trader = models.ForeignKey(TraderProfile, related_name='requirement_profiles')
	date_posted = models.DateField('Posted on', auto_now_add=True)
	categories = models.ManyToManyField(Category, related_name='requirement_profiles')
	notes = models.TextField('Notes', blank=True)

class RequirementProfileUpdate(models.Model):
	original_requirement = models.ForeignKey(RequirementProfile, related_name='requirement_profile_update_from')
	updated_requirement = models.ForeignKey(RequirementProfile, related_name='requirement_profile_update_to')
	date_updated = models.DateField('Date Updated', auto_now_add=True)
	trader = models.ForeignKey(TraderProfile)
	notes = models.TextField('Notes', blank=True)

class RequirementRecommendation(models.Model):
	is_active = models.BooleanField(default=True)
	requirement = models.ForeignKey(RequirementProfile, verbose_name='Requirement')
	core = models.ForeignKey(EquipmentCore, related_name='requirement_recommendations')
	trader = models.ForeignKey(TraderProfile, related_name='requirement_recommendations')
	date_recommendated = models.DateField('Date Recommended', auto_now_add=True)
	notes = models.TextField('Notes', blank=True)