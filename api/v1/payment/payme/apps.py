from django.apps import AppConfig


class PaymeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.payment.payme'
    label = 'payme'
