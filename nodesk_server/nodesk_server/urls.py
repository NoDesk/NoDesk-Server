from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nodesk_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    
    url(r'^template/', include('nodesk_template.urls_template')),
    url(r'^dossier/', include('nodesk_template.urls_dossier')),
    
    url(r'^auth/', include('nodesk_authentication.urls')),
    )
