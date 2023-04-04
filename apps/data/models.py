import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel
# Create your models here.

class Data(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default= uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name