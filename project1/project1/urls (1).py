from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project1.views.home', name='home'),
    # url(r'^project1/', include('project1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^add-to-db/$', 'Rate.views.add_view'),
    (r'^categories/$', 'Rate.views.cat_list'),
    (r'^entry/(?P<eID>\d+)/$', 'Rate.views.entry_detail'),
    (r'^entry_form/(?P<eID>\d+)/$', 'Rate.forms.entry_form'),
    (r'^rate/$', 'Rate.forms.rate_form'),
    (r'^rate2/(?P<eID>\d+)/$', 'Rate.forms.rate_formset'),
    (r'^rate3/(?P<pID>\d+)/$', 'Rate.forms.rate_form3'),

)
