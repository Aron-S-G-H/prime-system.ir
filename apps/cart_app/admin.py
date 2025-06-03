import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import UserOrder, ProductOrder
from django.urls import reverse
from django.utils.safestring import mark_safe
from jalali_date import datetime2jalali


# def user_invoice_pdf(order):
#     url = reverse('cart:admin_invoice_page', args=[order.id])
#     return mark_safe(f'<a href="{url}">PDF</a>')
#
#
# user_invoice_pdf.short_description = 'Export to PDF'


class ProductOrderAdmin(admin.StackedInline):
    model = ProductOrder
    extra = 0


@admin.register(UserOrder)
class UserOrderAdmin(admin.ModelAdmin):
    inlines = (ProductOrderAdmin,)
    list_filter = ('is_paid', 'is_sms_sent')
    list_display = ('user', 'phone', 'total_price', 'state', 'is_paid', 'is_sms_sent', 'created_at_jalali')
    readonly_fields = ('created_at_jalali', 'order_uuid')
    search_fields = ('first_name', 'last_name', 'phone')
    actions = ['export_as_csv']

    @admin.display(description='Created at', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')
    #
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta.verbose_name)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export as CSV"
