from django.contrib import admin
from .models import SliderBanner, SmallBanner, LargeBanner, Information, CompanyLogo, AboutUs, UploadFile


@admin.register(SliderBanner)
class SliderBannerAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'url', 'status')
    list_editable = ('status',)


@admin.register(SmallBanner)
class SmallBannerAdmin(admin.ModelAdmin):
    readonly_fields = ('size', 'height', 'width')
    list_display = ('image_preview', 'size', 'url', 'status')
    list_editable = ('status',)


@admin.register(LargeBanner)
class LargeBannerAdmin(admin.ModelAdmin):
    readonly_fields = ('size', 'height', 'width')
    list_display = ('image_preview', 'size', 'url', 'status')
    list_editable = ('status',)


@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ('short_address', 'email', 'call_center', 'phone_number', 'phone_number2')


@admin.register(CompanyLogo)
class CompanyLogoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'image_preview')


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    # form = UploadFileAdminForm
    list_display = ('__str__', 'size', 'absolute_url')
    readonly_fields = ('size', 'absolute_url')


admin.site.register(AboutUs)
