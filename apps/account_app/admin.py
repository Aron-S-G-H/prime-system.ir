from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from jalali_date import datetime2jalali


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("first_name", 'last_name', 'phone', 'email', 'last_login_jalali', 'date_joined_jalali', "is_staff")
    list_filter = ("is_staff", "is_active", "date_joined", "last_login")
    readonly_fields = ('last_login_jalali', 'date_joined_jalali')
    fieldsets = (
        (None, {"fields": ("password", 'last_login_jalali', 'date_joined_jalali')}),
        ('Personal information', {"fields": ('first_name', 'last_name', 'phone', 'email', )}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "first_name", "last_name", "phone", "email", "password1", "password2", "is_superuser", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email", "phone", "first_name", "last_name")
    ordering = ("-date_joined",)

    @admin.display(description='Last login', ordering='last_login')
    def last_login_jalali(self, obj):
        if obj.last_login:
            return datetime2jalali(obj.last_login).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='Date joined', ordering='date_joined')
    def date_joined_jalali(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%Y/%m/%d - %H:%M')
