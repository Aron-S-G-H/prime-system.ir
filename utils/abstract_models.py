from django.db import models
from django.utils.text import slugify


class BaseBannerModel(models.Model):
    url = models.URLField(null=True, blank=True, help_text='URL address to refer to a page')
    status = models.BooleanField(default=True, help_text='Display status')

    class Meta:
        abstract = True


class BaseCategoryModel(models.Model):
    title = models.CharField(max_length=50, help_text='50 Character')
    english_title = models.CharField(max_length=50, help_text='50 Character')
    slug = models.SlugField(blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.english_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
