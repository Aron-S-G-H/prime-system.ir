from django.db import models


class MetaMixin(models.Model):
    meta_description = models.CharField(max_length=150, help_text='150 Character')
    meta_keyword = models.CharField(max_length=150, help_text='150 Character', null=True)

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImagePropertyMixin(models.Model):
    width = models.PositiveSmallIntegerField(null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    size = models.FloatField(blank=True, help_text='in kilobytes')

    class Meta:
        abstract = True
