from django.shortcuts import render
from django.http import HttpResponse
import json
import time
from nodesk_template.models import *
from django.core.exceptions import ObjectDoesNotExist
import mimetypes

#check if the user requesting the template or one of its attachement
#is authorized to access it.
def is_authorized(template_id) :
    return True

def is_logged() :
    return True

def ping(request) :
    return HttpResponse(time.strftime("%c"))

def get_template_list(request) :
    response = HttpResponse()
    if is_logged() :
        list_type = request.GET.get('alive', None)
        if list_type is None :
            template_query_set = Template.objects.all()
        elif list_type == 'true' :
            template_query_set = Template.objects.filter(alive=True)
        elif list_type == 'false' :
            template_query_set = Template.objects.filter(alive=False)
        
        json_content = []
        for template in template_query_set :
            content = {}

            content['name'] = template.name
            content['pk'] = template.pk
            if request.GET.get('yaml','false') == 'true' :
                content['yaml'] = template.yaml
            
            json_content.append(content)
        
        response.write(json.dumps(json_content))
        response["Content-Type"] = "application/json"
    else :
        response["status"] = 401
    
    return response


def get_template(request, template_id) :
    response = HttpResponse()
    if is_logged() and is_authorized(template_id) :
        try :
            template = Template.objects.get(pk=template_id)
            response['Content-Disposition'] = \
                    'attachment; filename="{0}.yaml"'.format(template.name)
            response["Content-Type"] = "application/prs.yaml"
            response.write(template.yaml)
        except ObjectDoesNotExist :
            reponse = HttpResponseNotFound()
    else :
        response["status"] = 401
    
    return response


dossier_model_object_dict = {}
def get_dossier_model_object(template_id) :
    global dossier_model_object_dict
    if dossier_model_object_dict.get(template_id, None) is None :
        try :
            template = Template.objects.get(pk=template_id)
            model_name = template.name + '_' + template.yaml_hash
            ns = {}
            exec('model = ' + model_name, ns)
        except (NameError, ObjectDoesNotExist) as e :
            ns['model'] = None
        dossier_model_object_dict[template_id] = ns['model']
    return template_model_object_dict[template_id]


def get_dossier_list_all(request) :
    #return HttpResponse("get dossier list all")
    return HttpResponseNotFound()


def save_field_value_in_dossier(field_value_list,dossier_object):
    for (field,value) in field_value_list :
        setattr(dossier_object,field,value)


def get_dossier_list_post_new_dossier(request, template_id) :
    response = HttpResponse()
    if is_logged() :
        try :
            dossier_model = get_template_model_object(template_id)
            if dossier_model is not None :
                if request.method == 'GET':
                    json_content = []
                    dossier_queryset = dossier_model.objects.all()
                    for dossier in dossier_queryset :
                        content = {}
                        
                        content['name'] = dossier.dossier_name
                        content['date'] = dossier.dossier_date
                        content['pk'] = dossier.pk
                        
                        json_content.append(content)
                    
                    response.write(json.dumps(json_content))
                    response["Content-Type"] = "application/json"
                elif request.method == 'POST' :
                    body = json.load(request.body)
                    dossier = dossier_model()
                    save_field_value_in_dossier(body.items(),dossier)
                    dossier.full_clean()
                    dossier.save()

                    json_content = serializers.serialize('json', [dossier])                    
                    response.write(json_content)
                    response["Content-Type"] = "application/json"
                else :
                    raise Exception()
            else :
                raise Exception()
        except :
            response = HttpResponseNotFound()
    else :
        response["status"] = 401
    
    return response




def get_dossier_post_dossier(request, template_id, dossier_id) :
    response = HttpResponse()
    if is_logged() and is_authorized(template_id) :
        try :
            dossier_model = get_template_model_object(template_id)
            if dossier_model is not None :
                    dossier = dossier_model.objects.get(pk = dossier_id)
                    if request.method == 'GET' :
                        json_content = serializers.serialize('json', [dossier])
                        response.write(json_content)
                        response["Content-Type"] = "application/json"

                    #if its a POST request, it means the user want to modify the dossier
                    #so we save the new value into its object, ans send a code 200
                    elif request.method == 'POST' :
                        if request["Content-Type"] == "application/json"
                            body = request.body
                            if isinstance(body,dict) : body = body.items()
                            
                            save_field_value_in_dossier(body,dossier)
                            dossier.full_clean() #XXX Is it a good idea to do that?
                            dossier.save()
                        elif request["Content-Type"] == "multipart/form-data" :
                            for file in request.FILES :
                                setattr(dossier, file, request.FILES[file])
                            dossier.save()
                        else :
                            raise Exception()
                    else :
                        raise Exception()
            else :
                raise Exception()
        except :
            response = HttpResponseNotFound()
    else :
        response["status"] = 401
    return response


def dehydrate(file_field):
    ret = None
    if isinstance(file_field,FieldFile) :
        try:
            content_type, encoding = mimetypes.guess_type(file_field.file.name)
            b64 = file_field.open().read().encode("base64")
            ret = {
                "name": os.path.basename(file_field.name),
                "size" : file_field.size,
                "file": b64,
                "content-type": content_type or "application/octet-stream"
            }
        except:
            ret = None
    return ret


def get_field_value_post_field_value(request, template_id, dossier_id, field_name) :
    response = HttpResponse()
    if is_logged() and is_authorized(template_id) :
        try :
            dossier_model = get_template_model_object(template_id)
            if dossier_model is not None :
                dossier = dossier_model.objects.get(pk = dossier_id)
                field = getattr(dossier,field_name)
                #field now contain the field object
                if request.method == 'GET':
                    #If it's a file field, we generate the base64 equivalent and write it
                    if isinstance(field,FieldFile) :
                        attachement = dehydrate(field)
                        response.write(attachement['file'])
                        response['Content-Type'] = attachement['content-type']
                        response['Content-Disposition'] = \
                                'attachment; filename="{0}"'.format(attachement['name'])
                        reponse['Content-Length'] = attachement['size']
                        #Handle last modified/ if modified since TODO ?
                    else :
                        #getting a non-FieldFile field is not allowed here
                        #It should be done with get_dossier_post_dossier
                        response = HttpResponse(status_code=501)
#                elif request.method == 'POST' :
#                    if isinstance(field,FieldFile) :
#                        #OLDTODO
#                        pass
#                    else :
#                        #setting a non-FieldFile field is not allowed here
#                        #It should be done with get_dossier_post_dossier
#                        response = HttpResponse(status_code=501)
                else :
                    raise Exception()
            else :
                raise Exception()                
        except :    
            response = HttpResponseNotFound()
    else :
        response["status"] = 401
    return response
