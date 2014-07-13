from django.db import models


class Template(models.Model):
    yaml_hash = models.CharField(
            max_length=64,
            unique=True)
    model_hash = models.CharField(
            max_length=64)
    name = models.CharField(
            max_length=100)
    yaml = models.TextField()
    model = models.TextField()
    alive = models.BooleanField(
            default=False)
    class Meta:
        app_label = 'nodesk_template'
