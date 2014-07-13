from django.shortcuts import render
from django.http import HttpResponse
import json


#check if the user requesting the template or one of its attachement
#is authorized to access it.
def is_authorized(template_id) :
    return True

def is_logged() :
    return True



def get_template_list(request) :
    response = HttpResponse()
    if is_logged() :
        json_content = []
        list_type = request.GET.get('alive', None)
        if list_type is None :
            template_query_set = Template.objects.all()
        elif list_type == 'true' :
            template_query_set = Template.objects.filter(alive=True)
        elif list_type == 'false' :
            template_query_set = Template.objects.filter(alive=False)
        
        for template in template_query_set :
            content = {}
            content['name'] = template.name
            content['id'] = template.name
            if request.GET.get('yaml','false') == 'true' :
                content['yaml'] = template.yaml
            json_content.append(content)
        
        response.write(json.dumps(content))
        response["content_type"] = "application/json"
    else :
        response["status"] = 401
    
    return response


def get_template(request, template_id) :
    response = HttpResponse()
    if is_logged() and is_authorized(template_id) :
        template = Template.objects.get(id=template_id)
        if template is not None :
            response['Content-Disposition'] = \
                    'attachment; filename="{0}"'.format(template.name)
            response["content_type"] = "application/prs.yaml"
            response.write(template.yaml)
        else :
            response["status"] = 404
    else :
        response["status"] = 401
    
    return response





def get_dossier_list_all(request) :
    return HttpResponse("get dossier list all")

def get_dossier_list(request, template_id) :
    return HttpResponse("get dossier list for template :" + template_id)

def get_dossier(request, template_id, dossier_id) :
    return HttpResponse("get dossier " + dossier_id + " from template " + template_id)

def get_dossier_attachement(request, template_id, dossier_id, attachement_id) :
#    response = HttpResponse("lol", content_type='application/vnd.ms-excel')
#    response['Content-Disposition'] = 'attachment; filename="foo.xls"'
    return HttpResponse("get attachement " + attachement_id + " from dossier " + dossier_id + " from template " + template_id)

def add_new_dossier(request, template_id) :
    return HttpResponse("Add new dossier with template " + template_id)
