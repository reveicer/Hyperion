from django.conf.urls import patterns, include, url
from Hyperion.apps.htraders import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^dashboard/$', 'Hyperion.apps.htraders.views.dashboard'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
