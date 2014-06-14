import yaml
import hashlib
#import bencode

from django.db import models

def generateModelFromYAML(file_path) :
    attrs = {
        'name': models.CharField(max_length=32),
        '__module__': 'nodesk_server.models'
    }
    Animal = type("Animal", (models.Model,), attrs)
    return Animal


    
