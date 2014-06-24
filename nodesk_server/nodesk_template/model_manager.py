#from django.db import models

import yaml
import hashlib
import os

import nodesk_template.models
from nodesk_template.exceptions import UnrecognizedFieldType
from nodesk_template.constants import INDENTATION

from field_types import field_types



APP_NAME = "nodesk_template"


def generate_model_from_YAML(file_path) :
    template_yaml = yaml.load(open(file_path,'r').read())

    #Hash the content of the yaml file/dump produced by PyYAML (equivalent)

    template_hash = hashlib.sha256( yaml.dump(template_yaml) ).hexdigest()

    #Get the name of the yaml file (with extension) from the path of the file
    filename = os.path.basename(file_path)
    #Get the name of the yaml file without the extension
    filename, _ = os.path.splitext(filename)
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

        model_path = '{1}/{2}'.format(nodesk_template.models.path[0], filename)
        with open(model_path, 'w') as model_file:
            model_file.write(get_header(filename))

            for field in template_yaml:
                if (field['type'] == 'Section'):
                    for field_ in field['value']:
                        func = field_types.get(field['type'], None)
                        if func is None:
                            raise UnrecognizedFieldType(field['type'], field['name'])

                        model_file.write(func(field_['value']))

                else:
                    func = field_types.get(field['type'], None)
                    if model_string is None:
                        raise UnrecognizedFieldType(field['type'], field['name'])

                    model_file.write(func(field['value']))

                model_file.write(get_meta_class)
        return template


def get_header(class_name):
    return """from django.db import models

class {1}(models.Model):
""".format(class_name)

def get_meta_class(file) :
    file.write('\n'*4)
    file.write(INDENTATION + "class Meta:\n")
    file.write(INDENTATION*2 + "\"\"\"Meta Class for your model.\"\"\"\n")
    file.write(INDENTATION*2 + "app_label = '%s'\n" % APP_NAME)


