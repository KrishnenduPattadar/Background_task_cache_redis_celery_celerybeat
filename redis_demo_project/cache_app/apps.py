from django.apps import AppConfig


class CacheAppConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'cache_app'


    def ready(self):
        import cache_app.signals
