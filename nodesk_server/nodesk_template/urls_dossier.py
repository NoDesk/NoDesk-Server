from django.conf.urls import patterns, url

from nodesk_template import views

urlpatterns = patterns(
        '',
        url(
            r'^/?$',
            views.get_dossier_list_all),
        url(
            r'^/(?P<template_id>[0-9]+)/?$',
            views.get_dossier_list) ,
        url(
            r'^/(?P<template_id>[0-9]+)/'
            '(?P<dossier_id>[0-9]+)/?$',
            views.get_dossier),
        url(
            r'^/(?P<template_id>[0-9]+)/'
            '(?P<dossier_id>[0-9]+)/'
            '(?P<attachement_field_name>.+)/?$',
            views.get_dossier_attachement),
        url(
            r'^/(?P<template_id>[0-9]+)/'
            'new/?$' ,
            views.add_new_dossier),
        )
