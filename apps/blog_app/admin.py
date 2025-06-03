from django.contrib import admin
from .models import BlogPost, BlogPoster, BlogTag, BlogCategory, BlogComment
from jalali_date import datetime2jalali
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogPosterAdmin(admin.StackedInline):
    model = BlogPoster
    readonly_fields = ('width', 'height', 'size')
    extra = 1
    max_num = 1


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    inlines = (BlogPosterAdmin,)
    readonly_fields = ('created_at_jalali', 'update_at_jalali', 'slug')
    list_display = ('title', 'author', 'category', 'publish', 'created_at_jalali', 'update_at_jalali')
    list_filter = ('category', 'publish')
    list_editable = ('publish',)
    search_fields = ('title', 'english_title')
    filter_horizontal = ('tags',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super(BlogPostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description='Created at', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='Updated at', ordering='update_at')
    def update_at_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('name', 'slug')


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('name', 'slug')


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at_jalali',)
    list_display = ('blog', 'user', 'has_reply', 'created_at_jalali')

    @admin.display(description='Created at', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')
