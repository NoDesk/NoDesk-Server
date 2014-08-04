from django.contrib import admin

from models import *

import models
import inspect
from django.db.models.base import ModelBase
from django.contrib.admin.sites import AlreadyRegistered


for name, obj in inspect.getmembers(models ):
    if inspect.isclass(obj):
        if isinstance(obj, ModelBase):
            if not obj._meta.abstract:
                try:
                    admin.site.register(obj)
                except AlreadyRegistered:
                    pass

