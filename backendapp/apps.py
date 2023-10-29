from django.apps import AppConfig

class BackendAppConfig(AppConfig):
    name = 'backendapp'

    def ready(self):
        import backendapp.signals