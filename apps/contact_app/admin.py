from django.contrib import admin
from .models import ContactUs
from jalali_date import datetime2jalali


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'created_at_jalali')
    list_display = ('user', 'short_message', 'created_at_jalali')
    ordering = ('-created_at',)

    @admin.display(description='Created at', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')
