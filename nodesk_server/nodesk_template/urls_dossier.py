from django.conf.urls import patterns, url

from nodesk_template import views

urlpatterns = [
        url(r'^ping', views.ping),
        url(
            r'^$',
            views.get_dossier_list_all),
        url(
            r'^(?P<template_id>[0-9]+)/?$',
            views.get_dossier_list_post_new_dossier) ,
        url(
            r'^(?P<template_id>[0-9]+)/'
            '(?P<dossier_id>[0-9]+)/?$',
            views.get_dossier_post_dossier),
        url(
            r'^(?P<template_id>[0-9]+)/'
            '(?P<dossier_id>[0-9]+)/'
            '(?P<field_name>.+)/?$',
            views.get_field_value_post_field_value),
        ]
