from django.shortcuts import render, render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import *
from django.http import *
from django.core.exceptions import *
from django.forms.formsets import formset_factory
from nodesk_admin import forms
from nodesk_server import settings
import nodesk_template
from nodesk_template import model_manager, models
import time, os, re, yaml

TemplateFieldFormSet = formset_factory(forms.TemplateFieldForm)
TemplateFieldFormSet_noExtra = formset_factory(forms.TemplateFieldForm,extra=0)
TemplateConfigFormSet = formset_factory(forms.TemplateConfigForm,extra=0)

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
    initial_data = models.Template.objects.order_by('visible','name','id').values('id','name','visible')
    template_config_formset = TemplateConfigFormSet(initial=initial_data)
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
               'template_form' : template_form,
               'template_config_formset' : template_config_formset})


@staff_member_required
@require_POST
def template_config_save(request):
    msg = {'redirect_url':'/admin/nodesk/', 'error':True}
    try :
        if 'save' in request.POST :
            formset = TemplateConfigFormSet(request.POST,request.FILES)
            if formset.is_valid() :
                templates = {x.pk : x for x in models.Template.objects.all()}
                for form in formset :
                    id = int(form.cleaned_data['id'])
                    name = form.cleaned_data['name']
                    visible = form.cleaned_data['visible']
                    template = templates.get(id,None)
                    if template is not None :
                        if (template.name != name) or (template.visible != visible) :
                            template.visible = visible
                            template.name = name
                            template.full_clean()
                            template.save()
    except :
        msg['content'] = "An error occured during the save of the templates' configuration."
        if settings.DEBUG : raise
    else :
        msg['content'] = 'Configurations for the templates correctly saved.'
        msg['success'] = True
        del msg['error']
    return render(request,'nodesk_admin/redirect.html', msg)


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
                'content':'LDAP configuration saved. The server is now reloading.',
                'success':True})

@staff_member_required
@require_POST
def template_save(request):
    filepath = ""
    msg = {'redirect_url':'/admin/nodesk/', 'error':True}
    try :
        if 'template_save' in request.POST :
            form = forms.TemplateSaveForm(request.POST)
            if form.is_valid() :

                template_object = model_manager.generate_template_model_from_YAML_with_name(
                        form.cleaned_data['template_content'],
                        form.cleaned_data['template_name'])
                template_object.full_clean()
                template_object.save()
                model_manager.sync_model()
                reload_uwsgi()
    except :
        msg['content'] = "An error occured during the save of the template. Maybe an error in the YAML?"
        if settings.DEBUG : raise
    else :
        msg['content'] = 'Template correctly saved. The server is now reloading.'
        msg['success'] = True
        del msg['error']
    return render(request,'nodesk_admin/redirect.html', msg)

@staff_member_required
def template_creator(request,template_id=None):
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
        return HttpResponseRedirect("/admin/nodesk/#template_save")
    else :
        if template_id is None :
            formset = TemplateFieldFormSet()
        else :
            try :
                template = models.Template.objects.get(pk=template_id)
                fields = yaml.load(template.yaml)
                data = []
                for field in fields :
                    field_data = {
                            'field_name': field['name'],
                            'field_type':field['type'],
                            'field_value': field['value'] #TODO FIXME
                            }
                    #TODO FIXME
                    if field.get('options',None) is not None :
                        field_data['field_options'] = field['options']
                    data.append(field_data)
                print data
                formset = TemplateFieldFormSet_noExtra(initial=data)
            except ObjectDoesNotExist:
                formset = TemplateFieldFormSet()
        return render(request,'nodesk_admin/template_creator.html',
                {'field_formset':formset})

@staff_member_required
def reload_server(request) :
    reload_uwsgi()
    return render(request,'nodesk_admin/redirect.html',
            {
                'redirect_url':'/admin/nodesk/',
                'content': "Reloading server",
                'success':True})
