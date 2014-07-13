from django.conf.urls import patterns, url

from nodesk_template import views

urlpatterns = patterns(
        '',
        url(r'^/?$', views.get_template_list),
        url(r'^/(?P<template_id>[a-zA-Z0-9]+)/?$', views.get_template),
    )
