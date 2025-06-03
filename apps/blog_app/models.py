from django.db import models
from django.contrib.auth import get_user_model
from utils.mixins import TimeStampMixin, MetaMixin, ImagePropertyMixin
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.urls import reverse


User = get_user_model()


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='100 Character')
    english_name = models.CharField(max_length=100, unique=True, help_text='100 Character')
    slug = models.SlugField(max_length=100, unique=True, blank=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.english_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogTag(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text='50 Character')
    english_name = models.CharField(max_length=50, unique=True, help_text='50 Character')
    slug = models.SlugField(max_length=50, unique=True, blank=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.english_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(TimeStampMixin, MetaMixin, models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='blogs')
    title = models.CharField(max_length=255, unique=True, help_text='255 Character')
    english_title = models.CharField(max_length=255, unique=True, help_text='255 Character')
    introduction = models.TextField()
    description = CKEditor5Field(config_name='extends')
    tags = models.ManyToManyField(BlogTag, related_name='blogs')
    publish = models.BooleanField(default=True)
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def average_rating(self):
        comments = self.comments.filter(rating__gt=0)
        if comments.exists():
            rating_avg = comments.aggregate(models.Avg('rating'))['rating__avg']
            return round(rating_avg, 1)
        return 0.0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.english_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogPoster(ImagePropertyMixin, models.Model):
    blog = models.OneToOneField(BlogPost, on_delete=models.CASCADE, related_name='poster')
    poster = models.ImageField(upload_to='blog-image', width_field='width', height_field='height', help_text='822 × 522 px')

    def save(self, *args, **kwargs):
        self.size = self.poster.size / 1000
        super(BlogPoster, self).save(*args, **kwargs)

    def __str__(self):
        return mark_safe(f'<img src = "{self.poster.url}" width = "100"/>')


class BlogComment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def has_reply(self):
        if self.parent:
            return True
        else:
            return False
    has_reply.short_description = 'has reply'

    def __str__(self):
        return f'{self.user} - {self.text[:20]}'
