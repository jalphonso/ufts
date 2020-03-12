from django.apps import AppConfig


class DayoneConfig(AppConfig):
    name = 'dayone'

    def ready(self):
        import dayone.signals
