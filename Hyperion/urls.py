from django.conf.urls import patterns, include, url
import Hyperion.apps.htraders.views
import Hyperion.apps.hcustomers.views
import Hyperion.apps.hinventory.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^dashboard/$', 'Hyperion.apps.htraders.views.dashboard', name='dashboard'),
	
	# account urls
	url(r'^account/login/$', Hyperion.apps.htraders.views.LoginView.as_view(), name='account_login'),
	url(r'^account/signup/$', Hyperion.apps.htraders.views.SignupView.as_view(), name='account_signup'),
 	url(r'^account/', include('account.urls')),

 	# profile urls
	url(r'^profile/company/(?P<company_id>\d+)/$', 'Hyperion.apps.hcustomers.views.company_profile'),
	url(r'^profile/contact/(?P<contact_id>\d+)/$', 'Hyperion.apps.hcustomers.views.contact_profile'),
	url(r'^profile/register/company/$', 'Hyperion.apps.hcustomers.views.register_company'),
	url(r'^profile/register/contact/(?P<company_id>\d+)/$', 'Hyperion.apps.hcustomers.views.register_contact'),
	#url(r'^profile/equipment/(?P<equipment_id>\d+)/$', 'Hyperion.apps.hinventory.views.equipment_profile'),

	# admin urls
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
