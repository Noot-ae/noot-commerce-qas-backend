from django.apps import AppConfig


class PageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'page'

    def ready(self) -> None:
        import page.signals