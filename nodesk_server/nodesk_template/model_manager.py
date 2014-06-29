#from django.db import models
import yaml
import hashlib
import os

import nodesk_template.models
from nodesk_template.exceptions import UnrecognizedFieldType
from nodesk_template.constants import INDENTATION

from field_types import field_types_dict

APP_NAME = "nodesk_template"


def generate_template_model_from_YAML_string(file_content, filename):
    template_yaml = yaml.load(file_content)

    #Hash the content of the yaml file/dump produced by PyYAML (equivalent)
    template_hash = hashlib.sha256(yaml.dump(template_yaml)).hexdigest()

    #Get the name of the yaml file without the extension
    filename = os.path.splitext(filename)[0]
    filename = filename + "_" + template_hash

    #FIXME
    #template = Template.objects.get(hash__exact=template_hash)
    template = None

    #May check that the model file was also created
    if template is None:
        #FIXME
        #template = Template(
        #        hash=template_hash,
        #        name=filename,
        #        yaml=template_yaml.dump())
        #template.save()
        pass

    model_path = '{0}/{1}.py'.format(nodesk_template.models.__path__[0],
                                  filename)
    with open(model_path, 'w') as model_file:
        model_file.write(get_header(filename))
        for field in template_yaml:
            if (field['type'] == 'Section'):
                for field_ in field['value']:
                    func = field_types_dict.get(field['type'], None)
                    if func is None:
                        raise UnrecognizedFieldType(field_['value'])

                    model_file.write(func(field_['name'], field_['value']))

            else:
                func = field_types_dict.get(field['type'], None)
                if func is None:
                    raise UnrecognizedFieldType(field['type'])

                model_file.write(func(field['name'], field['value']))

        model_file.write(get_meta_class())
    return template


def get_header(class_name):
    return """from django.db import models

class {0}(models.Model):
""".format(class_name)


def get_meta_class():
    return '\n'*2 + INDENTATION + "class Meta:\n" + INDENTATION*2 + \
        "\"\"\"Meta Class for your model.\"\"\"\n" + \
        INDENTATION*2 + "app_label = '%s'\n" % APP_NAME


def generate_template_model_from_YAML_file(file_path):
    filename = os.path.basename(file_path)
    content = ""
    with open(file_path, "r") as file_:
        content = file_.read()
    return generate_template_model_from_YAML_string(content, filename)


#Generate a template from a tuple of the Templates table
def generate_template_model_from_Template(template):
    return generate_template_model_from_YAML_string(
            template.yaml,
            template.name)

