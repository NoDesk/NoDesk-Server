from django.shortcuts import render
from django.core import serializers
from django.http import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.files import *
from django.views import static

from django.views.decorators.csrf import csrf_exempt 

import json
import time

from nodesk_template.models import *
from nodesk_server import settings

#check if the user requesting the template or one of its attachement
#is authorized to access it.
def is_authorized(template_id) :
    return True

def is_logged(request) :
    return request.user.is_authenticated()

def ping(request) :
    return HttpResponse(time.strftime("%c"))

def get_template_list(request) :
    response = HttpResponse()
    if is_logged(request) :
        list_type = request.GET.get('visible', None)
        if list_type is None :
            template_query_set = Template.objects.all()
        elif list_type == 'true' :
            template_query_set = Template.objects.filter(visible=True)
        elif list_type == 'false' :
            template_query_set = Template.objects.filter(visible=False)
        
        json_content = []
        for template in template_query_set :
            content = {}

            content['name'] = template.name
            content['pk'] = template.pk
            if is_authorized(template.pk) and request.GET.get('json','false') == 'true' :
                content['json'] = template.json
            
            json_content.append(content)
        
        response.write(json.dumps(json_content))
        response["Content-Type"] = "application/json"
    else :
        response = HttpResponse(status = 401)
    
    return response


def get_template(request, template_id) :
    response = HttpResponse()
    if is_logged(request) and is_authorized(template_id) :
        try :
            template = Template.objects.get(pk=template_id)
            response['Content-Disposition'] = \
                    'attachment; filename="{0}.json"'.format(template.name)
            response["Content-Type"] = "application/json"
            response.write(template.json)
        except ObjectDoesNotExist :
            reponse = HttpResponseNotFound()
            if settings.DEBUG is True : raise
    else :
        response = HttpResponse(status = 401)
    
    return response


dossier_model_object_dict = {}
def get_dossier_model_object(template_id) :
    global dossier_model_object_dict
    if dossier_model_object_dict.get(template_id, None) is None :
        try :
            template = Template.objects.get(pk=template_id)
            model_name = template.name + '_' + template.yaml_hash
            exec('model = ' + model_name)
        except (NameError, ObjectDoesNotExist) as e :
            model = None
        dossier_model_object_dict[template_id] = model
    return dossier_model_object_dict[template_id]


def get_dossier_list_all(request) :
    #return HttpResponse("get dossier list all")
    return HttpResponseNotFound()


def save_field_value_in_dossier(field_value_list,dossier_object):
    for (field,value) in field_value_list :
        setattr(dossier_object,field,value)


def get_dossier_list_post_new_dossier(request, template_id) :
    response = HttpResponse()
    if is_logged(request) :
        try :
            dossier_model = get_dossier_model_object(template_id)
            if dossier_model is not None :
                if request.method == 'GET':
                    json_content = []
                    dossier_queryset = dossier_model.objects.all()
                    for dossier in dossier_queryset :
                        content = {}
                        
                        content['name'] = str(dossier.dossier_name)
                        content['date'] = str(dossier.dossier_date)
                        content['pk'] = str(dossier.pk)
                        
                        json_content.append(content)
                    
                    response.write(json.dumps(json_content))
                    response["Content-Type"] = "application/json"
                elif request.method == 'POST' :
                    if "application/json" in request.META["CONTENT_TYPE"] :
                        body = json.loads(request.body)
                        dossier = dossier_model()
                        #create the dossier ahead of time, to generate a pk for it
                        dossier.save()
                        save_field_value_in_dossier(body.items(),dossier)
                        dossier.full_clean()
                        dossier.save()

                        json_content = serializers.serialize('json', [dossier])                    
                        response.write(json_content)
                        response["Content-Type"] = "application/json"
                    #elif "multipart/form-data" in request.META["CONTENT_TYPE"] :
                        #FIXME
                        ##create the dossier ahead of time, to generate a pk for it
                        #dossier.save()
                        #for file in request.FILES :
                        #    setattr(dossier, file, request.FILES[file])
                        #dossier.save()
                        pass
                    else :
                        raise Exception()
                else :
                    raise Exception()
            else :
                raise Exception()
        except :
            response = HttpResponseNotFound()
            if settings.DEBUG is True : raise
    else :
        response = HttpResponse(status = 401)
    
    return response



def get_dossier_post_dossier(request, template_id, dossier_id) :
    response = HttpResponse()
    if is_logged(request) and is_authorized(template_id) :
        try :
            dossier_model = get_dossier_model_object(template_id)
            if dossier_model is not None :
                    dossier = dossier_model.objects.get(pk = dossier_id)
                    if request.method == 'GET' :
                        json_content = serializers.serialize('json', [dossier])
                        response.write(json_content[1:-1])
                        response["Content-Type"] = "application/json"

                    #if its a POST request, it means the user want to modify the dossier
                    #so we save the new value into its object, ans send a code 200
                    elif request.method == 'POST' :
                        if "application/json" in request.META["CONTENT_TYPE"] :
                            body = request.body
                            if isinstance(body,str) : body = json.loads(body)
                            if isinstance(body,dict) : body = body.items()

                            save_field_value_in_dossier(body,dossier)
                            dossier.full_clean() #XXX Is it a good idea to do that?
                            dossier.save()
                        elif "multipart/form-data" in request.META["CONTENT_TYPE"] :
                            for file in request.FILES :
                                setattr(dossier, file, request.FILES[file])
                            dossier.save()
                        else :
                            raise Exception()
                    else :
                        raise Exception()
            else :
                raise Exception()
        except:
            response = HttpResponseNotFound()
            if settings.DEBUG is True : raise
    else :
        response = HttpResponse(status = 401)
    return response



def get_field_value_post_field_value(request, template_id, dossier_id, field_name) :
    response = HttpResponse()
    if is_logged(request) and is_authorized(template_id) :
        try :
            dossier_model = get_dossier_model_object(template_id)
            if dossier_model is not None :
                dossier = dossier_model.objects.get(pk = dossier_id)
                field = getattr(dossier,field_name)
                #field now contain the field object
                if request.method == 'GET':
                    #If it's a file field, we generate the base64 equivalent and write it
                    if isinstance(field,FieldFile) :
                        response = static.serve(request,field.path, "/")
                    else :
                        #getting a non-FieldFile field is not allowed here
                        #It should be done with get_dossier_post_dossier
                        response = HttpResponse(status=501)
#                elif request.method == 'POST' :
#                    if isinstance(field,FieldFile) :
#                        #OLDTODO
#                        pass
#                    else :
#                        #setting a non-FieldFile field is not allowed here
#                        #It should be done with get_dossier_post_dossier
#                        response = HttpResponse(status=501)
                else :
                    raise Exception()
            else :
                raise Exception()                
        except :
            response = HttpResponseNotFound()
            if settings.DEBUG is True : raise
    else :
        response = HttpResponse(status = 401)
    return response
