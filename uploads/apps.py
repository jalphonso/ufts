from django.apps import AppConfig


class UploadsConfig(AppConfig):
    name = 'uploads'

    def ready(self):
        import uploads.signals
