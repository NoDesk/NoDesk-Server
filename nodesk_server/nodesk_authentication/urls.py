from django.conf.urls import patterns, url

from nodesk_authentication import views

urlpatterns = [
        url(
            r'^ping',
            views.ping),
        url(
            r'^login/?$',
            views.login),
        url(
            r'^logout/?$',
            views.logout),
    ]

