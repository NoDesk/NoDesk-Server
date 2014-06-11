from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Post(models.Model):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, blank=True)
    message = models.CharField(max_length=512)

    def summary(self):
        return self.message[:50]
    def __unicode__(self):
        return self.summary()
