from django.db import models
import hashlib


class template(models.Model):
    name = models.CharField(max_length=100)
    yaml_hash = models.CharField(max_length=64)
    yaml = models.TextField()


