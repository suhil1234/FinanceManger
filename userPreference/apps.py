from django.apps import AppConfig


class UserpreferenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userPreference'

    def ready(self):
        import userPreference.signals