from django.shortcuts import render, render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import *
from django.http import *
from django.forms.formsets import formset_factory
from nodesk_admin import forms
from nodesk_server import settings
import nodesk_template
from nodesk_template import model_manager
import time, os, re, yaml


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def reload_uwsgi() :
    settings_path = re.sub('pyc$','py',os.path.abspath(settings.__file__))
    touch(settings_path)

@staff_member_required
@require_safe
def admin_console(request) :
    ldap_form = forms.ConfigLDAPForm()
    template_form = forms.TemplateSaveForm()
    if 'template_name' in request.session and 'template_content' in request.session :
        template_form = forms.TemplateSaveForm(
                initial=
                {
                    'template_name': request.session['template_name'],
                    'template_content': request.session['template_content'],
                })
        del request.session['template_name']
        del request.session['template_content']

    return render(request,'nodesk_admin/index.html',
            {
                'ldap_form' : ldap_form,
                'template_form' : template_form})

@staff_member_required
@require_POST
def ldap_config_save(request) :
    if 'custom_save' in request.POST or 'default_save' in request.POST :
        form = forms.ConfigLDAPForm(request.POST)
        if form.is_valid():
            with open(settings.SETTINGS_YAML_FILEPATH,'r+') as file_ :
                settings_yaml = yaml.load(file_.read())
                file_.seek(0)
                if 'custom_save' in request.POST :
                    form_data_dict = form.cleaned_data
                    for key in form_data_dict :
                        settings_yaml[key]['set'] = form_data_dict[key]
                elif 'default_save' in request.POST :
                    for key in settings_yaml :
                        settings_yaml[key]['set'] = settings_yaml[key]['default']
                yaml.safe_dump(settings_yaml,default_style="'", stream=file_)
                file_.truncate()
            reload(settings)
            reload(forms)
            reload_uwsgi()
    else :
        return HttpResponseRedirect("/admin/nodesk/")
    return render(request,'nodesk_admin/redirect.html',
            {
                'redirect_url':'/admin/nodesk/',
                'content':'LDAP configuration saved. The server is reloading',
                'success':True})

@staff_member_required
@require_POST
def template_save(request):
    filepath = ""
    msg = {'redirect_url':'/admin/nodesk/'}
    try :
        if 'template_save' in request.POST :
            form = forms.TemplateSaveForm(request.POST)
            if form.is_valid() :
                dirpath = nodesk_template.__path__[0] + '/template_yaml'
                filepath = dirpath +'/' + form.cleaned_data['template_name'] + '.yaml'
                with open(filepath,'w') as file_ :
                    file_.write(form.cleaned_data['template_content'])
                model_manager.sync_model(dirpath)
                reload_uwsgi()
    except :
        #os.remove(filepath)
        msg['content'] = "An error occured during the save of the template. Maybe an error in the YAML?"
        msg['error'] = True
        raise
    else :
        msg['content'] = 'Template correctly saved. The server is reloading'
        msg['success'] = True
    return render(request,'nodesk_admin/redirect.html', msg)

@staff_member_required
def template_creator(request):
    TemplateFieldFormSet = formset_factory(forms.TemplateFieldForm)
    if request.method == 'POST' :
        formset = TemplateFieldFormSet(request.POST,request.FILES)
        if formset.is_valid() :
            yaml_content = ""
            for form in formset :
                content = form.toNoDeskYAML()
                content = '-' + content[1:]
                yaml_content = yaml_content + content + '\n'
            request.session['template_name'] = request.POST[u'template_name']
            request.session['template_content'] = yaml_content
        else :
            return render(request,'nodesk_admin/redirect.html',
            {
                'redirect_url':'/admin/nodesk/template_creator/',
                'content': "A required field was missing",
                'error':True})
        return HttpResponseRedirect("/admin/nodesk/#template_creator")
    else :
        return render(request,'nodesk_admin/template_creator.html',
                {'field_formset':TemplateFieldFormSet()})

@staff_member_required
def reload_server(request) :
    reload_uwsgi()
    return render(request,'nodesk_admin/redirect.html',
            {
                'redirect_url':'/admin/nodesk/',
                'content': "Reloading server",
                'success':True})
