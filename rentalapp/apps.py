from django.apps import AppConfig


class RentalappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rentalapp'

    def ready(self):
        import rentalapp.signals
