#from django.db import models
import yaml
import json
import os

from django.core.management import call_command
import nodesk_template
from nodesk_template.models import Template
from nodesk_template.exceptions import UnrecognizedFieldType
from nodesk_template.constants import INDENTATION
from nodesk_template.crypto import hash_content
from nodesk_template.field_types import field_types_dict


APP_NAME = "nodesk_template"

def generate_field_name(initial_name, fieldnames_count_dict) :
    name = '_'.join(initial_name.split())
    fieldname_count = fieldnames_count_dict.get(name, 0)
    fieldnames_count_dict[name] = fieldname_count + 1
    return "{0}_{1}".format(name, fieldname_count)


def generate_template_model_from_YAML(yaml_python):
    model = None
    template_model = ""
   
    template_model = template_model + get_header() + get_static_fields()
    #if the name of the field is found multiple times in the yaml
    #we need to create fields in the model with unique name.
    #We will append to the field name its rank. This rank will be the last one+1
    #So we need to keep track of the count, and its done with this dict.
    fieldnames_count = {}
    for field in yaml_python:
        if field['type'] == 'Section' :
            for field_ in field['value']:
                func = field_types_dict.get(field['type'], None)
                if func is None:
                    raise UnrecognizedFieldType(field_['value'])
                field_name = generate_field_name(field_['name'], fieldnames_count)
                field['field_name'] = field_name
                template_model = template_model + func(field_name, field_['value'])

        else:
            func = field_types_dict.get(field['type'], None)
            if func is None:
                raise UnrecognizedFieldType(field['type'])

            field_name = generate_field_name(field['name'], fieldnames_count)
            field['field_name'] = field_name
            template_model = template_model + func(field_name, field.get('value',None))

    template_model = template_model + get_meta_class()

    return template_model


def get_header():
    return """from django.db import models
from nodesk_template.models.Template import Template

class {classname}(models.Model):
"""

def get_static_fields():
    list_field = []
    list_field.append(INDENTATION + "dossier_name = models.TextField()")
    list_field.append(INDENTATION + "dossier_date = models.DateField()")
    return '\n'.join(list_field) + '\n'


def get_meta_class():
    return '\n'*2 + INDENTATION + "class Meta:\n" + INDENTATION*2 + \
        "\"\"\"Meta Class for your model.\"\"\"\n" + \
        INDENTATION*2 + "app_label = '%s'\n" % APP_NAME


def generate_template_model_from_YAML_file(file_path):
    yaml_file = open(file_path, "r")
    yaml_string = yaml.dump(yaml.load(yaml_file.read()))
    yaml_file.close()

    #Hash the content of the yaml file/dump produced by PyYAML (equivalent)
    basename = os.path.splitext(os.path.basename(file_path))[0]
    yaml_hash = hash_content(yaml_string)
    
    yaml_python = yaml.load(yaml_string)
    model_content = generate_template_model_from_YAML(yaml_python)
    model_content = model_content.format(classname=basename.replace(' ','_') + "_" + yaml_hash )
    model_hash = hash_content(model_content)
    
    model = Template(
            yaml_hash=yaml_hash,
            model_hash=model_hash,
            name=basename,
            yaml=yaml.dump(yaml_python),
            json=json.dumps(yaml_python),
            model=model_content)
    return model



def sync_model(template_directory_path) :
    # For every Template in the db, we check that the model file is still there,
    # and if its content wasn't tampered with (we check the hash) :
    # if one of those two is true, then we re-write the model file content,
    # with the content saved in the Template
    # We also set 'visible' for all Template to false : if they are visible, they
    # will be set to true after that
    """
    for model in Template.objects.all().update(visible=False) :
        model_path = '{0}/{1}_{2}.py'.format(
                nodesk_template.models.__path__[0],
                model.name.replace(" ","_"),
                model.yaml_hash )
        if os.path.isfile(model_path) is False :
            with open(file_path, "w+") as model_file:
                model_hash = hash_content(model_file.read())
                if model.model_hash != model_hash:
                    model_file.seek(0)
                    model_file.write(model.model)
                    model_file.truncate()
    """


    # List the template files inside the template directory.
    # The list need to contain the path of the template files, not just their
    # filenames (that's why there's a call to map)
    file_list = os.listdir(template_directory_path)
    file_list = map(lambda x : template_directory_path + '/' + x , file_list)
    template_files = [ f for f in file_list if os.path.isfile(f) ]

    # For every template files, we check if a Template already exists for it.
    # if not, then we create the model and the Template corresponding to the
    # template file/yaml, save the Template and write the model down
    for template_file in template_files:
        with open(template_file, "r") as yaml_file :
            print template_file
            yaml_hash = hash_content(yaml.dump(yaml.load(yaml_file.read())))
            print template_file
        
        try:
            model = Template.objects.get(yaml_hash__exact=yaml_hash)
        except :
            model = None

        # if the model was not found in the db, that mean the yaml was never
        # parsed to generate de its model, so we generate the model
        if model is None:
            model = generate_template_model_from_YAML_file(template_file)

            model_path = '{0}/{1}_{2}.py'.format(
                    nodesk_template.models.__path__[0],
                    model.name.replace(" ","_"),
                    model.yaml_hash)
            with open(model_path, "w") as model_file:
                model_file.write(model.model)
        model.visible=True
        model.full_clean()
        model.save()
    reload(nodesk_template.models)
    call_command('syncdb', interactive=False)
