from django.apps import AppConfig


class DocumentationConfig(AppConfig):
    name = 'documentation'

    def ready(self):
        import documentation.signals
