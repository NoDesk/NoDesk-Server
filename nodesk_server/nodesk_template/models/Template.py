from django.db import models


class Template(models.Model):
    hash = models.CharField(
            max_length=64,
            primary_key=True)
    name = models.CharField(
            max_length=100,
            null=False)
    yaml = models.TextField()

    class Meta:
        app_label = 'nodesk_template'
