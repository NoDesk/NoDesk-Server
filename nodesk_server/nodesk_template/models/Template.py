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
    json = models.TextField()
    model = models.TextField()
    alive = models.BooleanField(
            default=False)
    
    @staticmethod
    def upload_to_func(template_hash):
        def func(instance, filename):
            return "{0}/{1}/{2}".format(template_hash,instance.pk,filename)
        return func
    
    class Meta:
        app_label = 'nodesk_template'
