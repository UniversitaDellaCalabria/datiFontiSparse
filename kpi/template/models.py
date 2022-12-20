from django.contrib.auth import get_user_model
from django.db import models


class ActivableModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CreatedModifiedBy(models.Model):
    created_by = models.ForeignKey(get_user_model(),
                                   null=True, blank=True,
                                   on_delete=models.SET_NULL,
                                   related_name='%(class)s_created_by')
    modified_by = models.ForeignKey(get_user_model(),
                                    null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='%(class)s_modified_by')

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
