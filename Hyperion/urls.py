from django.conf.urls import patterns, include, url
from Hyperion.apps.htraders import views
from Hyperion.apps.hcustomers import views
from Hyperion.apps.hinventory import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^dashboard/$', 'Hyperion.apps.htraders.views.dashboard'),
	url(r'^profile/company/(?P<company_id>\d+)/$', 'Hyperion.apps.hcustomers.views.company_profile'),
	url(r'^profile/contact/(?P<contact_id>\d+)/$', 'Hyperion.apps.hcustomers.views.contact_profile'),
	url(r'^profile/register/company/$', 'Hyperion.apps.hcustomers.views.register_company'),
	url(r'^profile/register/contact/(?P<company_id>\d+)/$', 'Hyperion.apps.hcustomers.views.register_contact'),
	url(r'^profile/equipment/(?P<equipment_id>\d+)/$', 'Hyperion.apps.hinventory.views.equipment_profile'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
