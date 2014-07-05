from django.db import models


class Template(models.Model):
    yaml_hash = models.CharField(
            max_length=64,
            primary_key=True)
    model_hash = models.CharField(
            max_length=64)
    name = models.CharField(
            max_length=100)
    yaml = models.TextField()
    model = models.TextField()

    class Meta:
        app_label = 'nodesk_template'
