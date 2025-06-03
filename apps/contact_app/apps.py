from django.apps import AppConfig


class ContactAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contact_app'
    verbose_name = 'Contact us'

    def ready(self):
        import apps.contact_app.signals
