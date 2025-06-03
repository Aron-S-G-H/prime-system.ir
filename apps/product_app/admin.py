from django.contrib import admin
from django.db import models
from .models import GeneralCategory, Category, Color, Product, ProductImage, ProductAttributeValue, ProductAttribute, ProductComment
from jalali_date import datetime2jalali
from django_json_widget.widgets import JSONEditorWidget


class CategoryHasIconFilter(admin.SimpleListFilter):
    title = 'has icon'
    parameter_name = 'has_icon'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(icon__isnull=False).exclude(icon='')
        if self.value() == 'No':
            return queryset.filter(icon__isnull=True) | queryset.filter(icon='')
        return queryset


class CategoryParentFilter(admin.SimpleListFilter):
    title = "parent category"
    parameter_name = "parent_category_id__exact"

    def lookups(self, request, model_admin):
        category = Category.objects.filter(parent_category__isnull=True)
        return [(obj.id, obj.title) for obj in category]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent_category_id__exact=self.value())


@admin.register(GeneralCategory)
class GeneralCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'english_title', 'image')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'english_title', 'general_category', 'parent_category', 'has_icon')
    list_filter = ('general_category', CategoryParentFilter, CategoryHasIconFilter)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent_category":
            kwargs["queryset"] = Category.objects.filter(parent_category__isnull=True)
        return super(CategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_color', 'color_display')


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    readonly_fields = ('width', 'height', 'size')
    extra = 1


class ProductAttributeValueAdmin(admin.StackedInline):
    model = ProductAttributeValue
    extra = 1


class ProductCommentAdmin(admin.StackedInline):
    readonly_fields = ('created_at',)
    model = ProductComment
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageAdmin, ProductAttributeValueAdmin, ProductCommentAdmin)
    readonly_fields = ('created_at_jalali', 'update_at_jalali')
    list_display = ('name', 'base_price', 'availability', 'second_hand', 'disable_order', 'quantity')
    list_filter = ('category', 'availability', 'color', 'second_hand')
    list_editable = ('availability', 'base_price', 'second_hand', 'disable_order', 'quantity')
    search_fields = ('name', 'english_name')
    filter_horizontal = ('color',)
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    @admin.display(description='Created at', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='Updated at', ordering='update_at')
    def update_at_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


admin.site.register(ProductAttribute)
