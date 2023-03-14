from django.apps import AppConfig


class ChacksappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cHacksApp'

    def ready(self) -> None:
        import cHacksApp.signals
