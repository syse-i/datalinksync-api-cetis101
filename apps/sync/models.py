from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class SyncContent(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    is_synced = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]