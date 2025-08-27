from django.apps import AppConfig


class ModuleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.apps.havasbook"

    def ready(self):
        print("==== Havasbook signals loaded ====")
        import core.apps.havasbook.signals.brand