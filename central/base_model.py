from django.db import models
import uuid
# from django.utils import timezone


class BaseModel(models.Model):
    """ Apps Base Model """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
