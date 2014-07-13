#from django.db import models
import yaml
from nodesk_template.crypto import hash_content
import os

from nodesk_template.models import *
from nodesk_template.exceptions import UnrecognizedFieldType
from nodesk_template.constants import INDENTATION

from field_types import field_types_dict

APP_NAME = "nodesk_template"


def generate_template_model_from_YAML(file_content):
    template_yaml = yaml.load(file_content)

    model = None
    template_model = ""
   
    template_model = template_model + get_header()
    for field in template_yaml:
        if (field['type'] == 'Section'):
            for field_ in field['value']:
                func = field_types_dict.get(field['type'], None)
                if func is None:
                    raise UnrecognizedFieldType(field_['value'])

                template_model = (
                    template_model + func(field_['name'], field_['value']))

        else:
            func = field_types_dict.get(field['type'], None)
            if func is None:
                raise UnrecognizedFieldType(field['type'])

            template_model = (
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
    
    model_content = generate_template_model_from_YAML(yaml_content)
    model_content.format( basename + "_" + yaml_hash )
    model_hash = hash_content(model_content)
    
    model = Template(
            yaml_hash=yaml_hash,
            model_hash=model_hash,
            name=basename,
            yaml=yaml_content,
            model=model_content)
    return model



def sync_model(template_directory_path):
    # List the template files inside the template directory.
    # The list need to contain the path of the template files, not just their
    # filenames (that's why there's a call to map)
    file_list = os.listdir(template_directory_path)
    file_list = map(lambda x : template_directory_path + '/' + x , file_list)
    template_files = [ f for f in file_list if os.path.isfile(f) ]


    # For every template files, we check if a Template already exists for it.
    # if not, then we create the model and the Template corresponding to the
    # template file/yaml, save the Template and write the model down
    # If the Template does exist, we check that the model file is still there,
    # and if its content wasn't tampered with (we check the hash) :
    # if one of those two is true, then we re-write the model file content,
    # with the content saved in the Template
    for template_file in template_files:
        with open(template_file, "r") as yaml_file :
            yaml_hash = hash_content(yaml.dump(yaml.load(yaml_file.read())))
        
        #FIXME
        #model = Template.objects.get(yaml_hash__exact=yaml_hash)
        model = None

        # if the model was not found in the db, that mean the yaml was never
        # parsed to generate de its model, so we generate the model
        if model is None:
            model = generate_template_model_from_YAML_file(template_file)
            #model.full_clean() #FIXME
            #model.save() #FIXME

            model_path = '{0}/{1}_{2}.py'.format(
                    nodesk_template.models.__path__[0],
                    model.name
                    model.yaml_hash)
            with open(model_path, "w") as model_file:
                model_file.write(model.model)


        #else if a model was found in the db, we check if the model file exist,
        #and if it does, if its content is the same (to avoid manual modif by
        #the users). If one of those two is false, then we rewrite the content
        #of the file
        else:
            model_path = '{0}/{1}_{2}.py'.format(
                    nodesk_template.models.__path__[0],
                    model.name
                    model.yaml_hash)
            if os.path.isfile(model_path) is False :
                with open(file_path, "w+") as model_file:
                    model_hash = hash_content(model_file.read())
                    if model.model_hash != model_hash:
                        model_file.seek(0)
                        model_file.write(model.model)
                        model_file.truncate()
