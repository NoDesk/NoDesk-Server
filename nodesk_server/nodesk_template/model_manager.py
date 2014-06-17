#from django.db import models

import yaml
import hashlib
import os

import nodesk_template.models
import nodesk_template.exceptions

from field_types import field_types



APP_NAME = "nodesk_template"


def generateModelFromYAML(file_path) :
    template = yaml.load(file_path)
    
    #Hash the content of the yaml file/dump produced by PyYAML (equivalent)
    template_hash = hashlib.sha256(template.dump()).hexdigest()

    #Get the name of the yaml file (with extension) from the path of the file
    filename = os.path.basename(file_path)
    #Get the name of the yaml file without the extension
    filename = os.path.splitext(filename)[0]

    if (Template.objects.get(hash__exact=template_hash)) is not None :
        pass #TODO
    else :
        pass #TODO


    model_file = open("%s/%s.py" % (nodesk_template.models.__path__,filename))
    template_model = ""
    for field in template :
        if (field['type'] == 'Section') :
            for field_ in field['value'] :
                function = field_types[field_['type']]
                if function is None :
                    raise UnrecognizedFieldType(field_['type'],field_['name'])
                else :
                    template_model_part = function(field_)
                    template_model = template_model + template_model_part
        
        
        else :
            function = field_types[field['type']]
            if function is None :
                raise UnrecognizedFieldType(field['type'],field['name'])
            else :
                template_model_part = function(field)
                template_model = template_model + template_model_part

    model_file.write(template_model + "\n")
    model_file.write("    class Meta:\n")
    model_file.write("        \"\"\"Meta Class for your model.\"\"\"\n")
    model_file.write("        app_label = '%s'\"\n" % APP_NAME)


