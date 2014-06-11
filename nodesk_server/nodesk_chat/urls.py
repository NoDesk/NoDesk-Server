from django.conf.urls import patterns, url

from nodesk_chat import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
