from utils.mixins import ImagePropertyMixin, TimeStampMixin
from utils.abstract_models import BaseBannerModel, models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import mark_safe
from django.template.defaultfilters import truncatewords
from django.conf import settings


class SliderBanner(BaseBannerModel):
    image = models.ImageField(upload_to='slider-banner', help_text='2048 × 427 px')
    phone_image = models.ImageField(upload_to='slider-banner/phone', help_text='To display in mobile size - 1780 × 890 px')

    def image_preview(self):
        return mark_safe(f'<img src = "{self.image.url}" width = "250"/>')
    image_preview.short_description = 'Image'

    def __str__(self):
        return self.image.url


class SmallBanner(ImagePropertyMixin, BaseBannerModel):
    image = models.ImageField(upload_to='small-banner', width_field='width', height_field='height', help_text='400 × 300 px')

    def image_preview(self):
        return mark_safe(f'<img src = "{self.image.url}" width = "100"/>')
    image_preview.short_description = 'Image'

    def save(self, *args, **kwargs):
        self.size = self.image.size / 1000
        super(SmallBanner, self).save(*args, **kwargs)

    def __str__(self):
        return self.image.url


class LargeBanner(ImagePropertyMixin, BaseBannerModel):
    image = models.ImageField(upload_to='large-banner', width_field='width', height_field='height', help_text='820 × 328 px')

    def image_preview(self):
        return mark_safe(f'<img src = "{self.image.url}" width = "130"/>')
    image_preview.short_description = 'Image'

    def save(self, *args, **kwargs):
        self.size = self.image.size / 1000
        super(LargeBanner, self).save(*args, **kwargs)

    def __str__(self):
        return self.image.url


class Information(models.Model):
    logo = models.ImageField(upload_to='logo', help_text='1000 × 300 px')
    address = models.CharField(max_length=150, null=True, blank=True, help_text='150 Character')
    email = models.EmailField(null=True, blank=True)
    call_center = models.CharField(max_length=11, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    phone_number2 = models.CharField(max_length=11, null=True, blank=True)
    telegram_id = models.CharField(max_length=50, null=True, blank=True, help_text='50 Character')
    instagram_id = models.CharField(max_length=50, null=True, blank=True, help_text='50 Character')

    def short_address(self):
        return truncatewords(self.address, 20)
    short_address.short_description = 'Address'

    def __str__(self):
        return truncatewords(self.address, 10)


class CompanyLogo(models.Model):
    company_name = models.CharField(max_length=30, help_text='30 Character')
    image = models.ImageField(upload_to='company-logo', help_text='600 × 284 px')

    def image_preview(self):
        return mark_safe(f'<img src = "{self.image.url}" width = "100"/>')
    image_preview.short_description = 'Logo'

    def save(self, *args, **kwargs):
        self.company_name = self.company_name.capitalize()
        super(CompanyLogo, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name


class AboutUs(TimeStampMixin, models.Model):
    title = models.CharField(max_length=60, help_text='60 Character')
    description = CKEditor5Field()

    class Meta:
        verbose_name_plural = 'About us'

    def __str__(self):
        return self.title


class UploadFile(models.Model):
    file = models.FileField(upload_to='uploaded-file', help_text='Only PDF, PNG and JPG')
    size = models.FloatField(blank=True, help_text='in kilobytes')
    absolute_url = models.URLField(blank=True)

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        domain_name = settings.ALLOWED_HOSTS[0]
        self.absolute_url = f'https://{domain_name}/public/media/uploaded-file/{self.file.name}'
        self.size = self.file.size / 1000
        super(UploadFile, self).save()
