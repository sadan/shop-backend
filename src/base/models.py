from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Following attributes can be removed, but sometimes they are useful when data is updated from other process rather
    # than users.
    created_by = models.CharField(max_length=128, null=True, blank=True)
    modified_by = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        abstract = True
