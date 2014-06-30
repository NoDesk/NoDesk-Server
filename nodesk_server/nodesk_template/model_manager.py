#from django.db import models
import yaml
from nodesk_template.crypto import hash_content
import os

import nodesk_template.models
from nodesk_template.exceptions import UnrecognizedFieldType
from nodesk_template.constants import INDENTATION

from field_types import field_types_dict

APP_NAME = "nodesk_template"


def generate_template_model_from_YAML(file_content):
    template_yaml = yaml.load(file_content)

    #Hash the content of the yaml file/dump produced by PyYAML (equivalent)
    yaml_hash = hash_content(yaml.dump(template_yaml)

    #Get the name of the file without the extension
    filename = os.path.splitext(filename)[0]
    filename = filename + "_" + yaml_hash

    model = None
    template_model = ""
   
    template_model = template_model + get_header()
    for field in template_yaml:
        if (field['type'] == 'Section'):
            for field_ in field['value']:
                func = field_types_dict.get(field['type'], None)
                if func is None:
                    raise UnrecognizedFieldType(field_['value'])

                template_model = 
                    template_model + func(field_['name'], field_['value']))

        else:
            func = field_types_dict.get(field['type'], None)
            if func is None:
                raise UnrecognizedFieldType(field['type'])

            template_model =
                template_model + func(field['name'], field['value']))

    template_model = template_model + get_meta_class()

    return template_model


def get_header():
    return """from django.db import models

class {classname}(models.Model):
"""


def get_meta_class():
    return '\n'*2 + INDENTATION + "class Meta:\n" + INDENTATION*2 + \
        "\"\"\"Meta Class for your model.\"\"\"\n" + \
        INDENTATION*2 + "app_label = '%s'\n" % APP_NAME


def generate_template_model_from_YAML_file(file_path):
    yaml_file = open(file_path, "r")
    yaml_content = yaml.dump(yaml.load(yaml_file.read()))
    yaml_file.close()

    #Hash the content of the yaml file/dump produced by PyYAML (equivalent)
    basename = os.path.splitext(os.path.basename(file_path))[0]
    yaml_hash = hash_content(yaml_content)
    basename = basename + "_" + yaml_hash
    model_path = '{0}/{1}.py'.format(nodesk_template.models.__path__[0],
                                  basename)
    
    model = None
    with open(model_path,"w") as model_file:
        model_content = generate_template_model_from_YAML(yaml_content)
        model_content.format(classname=basename)
        model_file.write(model_content)
        model_hash = hash_content(model_content)
        
        model = Template(
                yaml_hash=yaml_hash,
                model_hash=model_hash,
                name=basename,
                yaml=yaml_content,
                model=model_content)
    return model



def sync_model(template_directory_path):
    template_files = [ f for f in os.listdir(template_directory_path)
                     if os.path.isfile(template_directory_path+f) ]

    for template_file in template_files:
        yaml_file = open(file_path, "r")
        yaml_hash = hash_content(yaml.dump(yaml.load(yaml_file.read())))
        yaml_file.close()
        
        #FIXME
        #model = Template.objects.get(yaml_hash__exact=yaml_hash)
        model = None

        # if the model was not found in the db, that mean the yaml was never
        # parsed to generate de its model, so we generate the model
        if model is None:
            model = generate_template_model_from_YAML_file(template_file)
            model.full_clean()
            model.save()
        
        #else if a model was found in the db, we check if the model file exist,
        #and if it does, if its content is the same (to avoid manual modif by
        #the users). If one of those two is false, then we rewrite the content
        #of the file
        else:
            model_path = '{0}/{1}.py'.format(nodesk_template.models.__path__[0],
                                  model.name)
            if os.path.isfile(model_path) is not True
                with open(file_path, "w+") as model_file:
                    model_hash = hash_content(model_file.read())
                    if model.model_hash != model_hash:
                        model_file.seek(0)
                        model_file.write(model.model)
                        model_file.truncate()
