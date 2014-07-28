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
            response["status"] = 404
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
    return HttpResponse(status = 404)


def get_dossier_list(request, template_id) :
    response = HttpResponse()
    if is_logged() :
        dossier_model = get_template_model_object(template_id)
        if dossier_model is not None :
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
        else :
            response['status'] = 404
    else :
        response["status"] = 401
    
    return response




def get_dossier(request, template_id, dossier_id) :
    response = HttpResponse()
    if is_logged() and is_authorized(template_id) :
        dossier_model = get_template_model_object(template_id)
        if dossier_model is not None :
            try :
                dossier = dossier_model.objects.get(pk = dossier_id)
                
                json_content = serializers.serialize('json', [dossier])
                
                response.write(json_content)
                response["Content-Type"] = "application/json"
            except ObjectDoesNotExist :
                response['status'] = 404
        else :
            response['status'] = 404
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


def get_dossier_attachement(request, template_id, dossier_id, attachement_field_name) :
    response = HttpResponse()
    if is_logged() and is_authorized(template_id) :
        dossier_model = get_template_model_object(template_id)
        if dossier_model is not None :
            try :
                dossier = dossier_model.objects.get(pk = dossier_id)
                exec('attachement_field = dossier.' + attachement_field_name)
                attachement = dehydrate(attachement_field)
                response.write(attachement['file'])
                response['Content-Type'] = attachement['content-type']
                response['Content-Disposition'] = \
                        'attachment; filename="{0}"'.format(attachement['name'])
                reponse['Content-Length'] = attachement['size']
                #Handle last modified/ if modified since TODO ?
            except (ObjectDoesNotExist,AttributeError) as e :
                response['status'] = 404
        else :
            response['status'] = 404
    else :
        response["status"] = 401
    return response


def add_new_dossier(request, template_id) :
    return HttpResponse("Add new dossier with template " + template_id)
