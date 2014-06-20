#from django.db import models

import yaml
import hashlib
import os

import nodesk_template.models
import nodesk_template.exceptions
from nodesk_template.constants import *

from field_types import field_types



APP_NAME = "nodesk_template"


def generate_model_from_YAML(file_path) :
    template_yaml = yaml.load(open(file_path,'r').read())
    
    #Hash the content of the yaml file/dump produced by PyYAML (equivalent)

    template_hash = hashlib.sha256( yaml.dump(template_yaml) ).hexdigest()

    #Get the name of the yaml file (with extension) from the path of the file
    filename = os.path.basename(file_path)
    #Get the name of the yaml file without the extension
    filename = os.path.splitext(filename)[0]
    filename = filename + "_" + template_hash

    #FIXME
    #template = Template.objects.get(hash__exact=template_hash)
    template = None

    #May check that the model file was also created
    if template is None :
        #FIXME
        #template = Template(
        #        hash=template_hash,
        #        name=filename,
        #        yaml=template_yaml.dump())
        #template.save()

        model_file = open("%s/%s.py" % 
                (nodesk_template.models.__path__[0],filename), 'w' )
        
        
        add_header_to_class(model_file,filename)

        for field in template_yaml :
            if (field['type'] == 'Section') :
                for field_ in field['value'] :
                    function = field_types[field_['type']]
                    if function is None : raise UnrecognizedFieldType(field_['type'],field_['name'])
                    else : function(field_,model_file)
            
            else :
                function = field_types[field['type']]
                if function is None : raise UnrecognizedFieldType(field['type'],field['name'])
                else : function(field,model_file)

        add_meta_to_class(model_file)
        model_file.close()
    return template


def add_header_to_class(file,class_name) :
    file.write("from django.db import models\n\n\n")
    file.write("class %s(models.Model) :\n" % class_name)
    

def add_meta_to_class(file) :
    file.write('\n'*4)
    file.write(IDENTATION + "class Meta:\n")
    file.write(IDENTATION*2 + "\"\"\"Meta Class for your model.\"\"\"\n")
    file.write(IDENTATION*2 + "app_label = '%s'\n" % APP_NAME)


