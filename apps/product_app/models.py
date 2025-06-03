from django.db import models
from utils.abstract_models import BaseCategoryModel
from utils.mixins import ImagePropertyMixin, TimeStampMixin, MetaMixin
from django_ckeditor_5.fields import CKEditor5Field
from colorfield.fields import ColorField
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe
from django.urls import reverse


User = get_user_model()


class GeneralCategory(BaseCategoryModel):
    title = models.CharField(max_length=30, unique=True, help_text='30 Character')
    english_title = models.CharField(max_length=30, unique=True, help_text='30 Character')
    image = models.ImageField(upload_to='general-category', null=True, blank=True)


class Category(BaseCategoryModel):
    general_category = models.ForeignKey(GeneralCategory, related_name='subs', on_delete=models.CASCADE)
    parent_category = models.ForeignKey('self', related_name='subs', on_delete=models.CASCADE, null=True, blank=True)
    icon = models.ImageField(upload_to='category', null=True, blank=True, help_text='64 × 64 px')

    def has_icon(self):
        return bool(self.icon)


class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_color = ColorField(default='#FF0000', unique=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['name', 'hex_color'], name='color-pallet')]

    def color_display(self):
        return mark_safe(f'<div style="width: 30px; height: 20px; background-color: {self.hex_color};"></div>')
    color_display.short_description = 'Color'

    def __str__(self):
        return f'{self.name} - {self.hex_color}'


class Product(TimeStampMixin, MetaMixin, models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255, db_index=True, help_text='255 Character')
    english_name = models.CharField(max_length=255, help_text='255 Character')
    introduction = CKEditor5Field(null=True, blank=True)
    description = CKEditor5Field(config_name='extends')
    specification = models.JSONField(null=True, blank=True)
    base_price = models.PositiveIntegerField()
    color = models.ManyToManyField(Color, blank=True, related_name='products')
    special_price = models.PositiveIntegerField(null=True, blank=True)
    special_price_time = models.DateTimeField(null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    availability = models.BooleanField(default=True)
    disable_order = models.BooleanField(default=False)
    second_hand = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('product:detail', kwargs={'slug': self.slug})

    def discount_percent(self):
        if self.special_price:
            discount_percent = ((self.base_price - self.special_price) * 100) / self.base_price
            return round(discount_percent)
        return None

    def average_rating(self):
        comments = self.comments.filter(rating__gt=0)
        if comments.exists():
            rating_avg = comments.aggregate(models.Avg('rating'))['rating__avg']
            return round(rating_avg, 1)
        return 0.0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.english_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(ImagePropertyMixin, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product', height_field='height', width_field='width', help_text='800 × 800 px')

    def save(self, *args, **kwargs):
        self.size = self.image.size / 1000
        super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return mark_safe(f'<img src = "{self.image.url}" width = "80"/>')


class ProductAttribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_comments')
    text = models.TextField()
    speciality = models.JSONField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user} - {self.text[:20]}'
