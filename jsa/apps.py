from django.apps import AppConfig


class JsaConfig(AppConfig):
    name = 'jsa'

    def ready(self):
        import jsa.signals
