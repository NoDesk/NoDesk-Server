#from django.db import models

import yaml
import hashlib
import os

from field_types import field_types


APP_NAME = "nodesk_template"


def generateModelFromYAML(file_path) :
    template = yaml.load(file_path)
    
    #Hash the content of the yaml file/dump produced by PyYAML (equivalent)
    template_hash = hash_engine = hashlib.sha256(template.dump()).hexdigest()

    #Get the name of the yaml file (with extension) from the path of the file
    filename = os.path.basename(file_path)
    #Get the name of the yaml file without the extension
    filename = os.path.splitext(filename)[0]


#TODO Check if field_types return a function (wrong type detected)
    template_model = ""
    for field in template :
        if (field['type'] == 'Section') :
            for field_ in field['value'] :
                template_model_part = field_types[field_['type']](field_)
                template_model = template_model + template_model_part
        else :
            template_model_part = field_types[field['type']](field)
            template_model = template_model + template_model_part

    write(template_model + "\n")
    write("    class Meta:\n")
    write("        \"\"\"Meta Class for your model.\"\"\"\n")
    write("        app_label = '%s'\"\n" % APP_NAME)


