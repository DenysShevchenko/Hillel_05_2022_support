from django.db import models


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updateed_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
