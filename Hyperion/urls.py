from django.conf.urls import patterns, include, url
import Hyperion.apps.htraders.views
import Hyperion.apps.hcustomers.views
import Hyperion.apps.hinventory.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	#url(r'^$', 'Hyperion.apps.htraders.views.search', name='search'),
	url(r'^search/$', 'Hyperion.apps.htraders.views.search', name='search'),
	
	# account urls
	url(r'^account/login/$', Hyperion.apps.htraders.views.LoginView.as_view(), name='account_login'),
	url(r'^account/signup/$', Hyperion.apps.htraders.views.SignupView.as_view(), name='account_signup'),
 	url(r'^account/', include('account.urls')),

 	# profile urls
	url(r'^profile/company/(?P<company_id>\d+)/$', 'Hyperion.apps.hcustomers.views.company_profile', name='company_profile'),
	url(r'^profile/contact/(?P<contact_id>\d+)/$', 'Hyperion.apps.hcustomers.views.contact_profile', name='contact_profile'),
	url(r'^register/company/$', 'Hyperion.apps.hcustomers.views.register_company', name='register_company'),
	url(r'^register/contact/(?P<company_id>\d+)/$', 'Hyperion.apps.hcustomers.views.register_contact', name='register_contact'),
	#url(r'^profile/equipment/(?P<equipment_id>\d+)/$', 'Hyperion.apps.hinventory.views.equipment_profile'),

	# POST request urls
	url(r'^profile/contact/(?P<contact_id>\d+)/register/correspondence/$', 'Hyperion.apps.hcustomers.views.register_correspondence', name='register_correspondence'),

	# admin urls
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
