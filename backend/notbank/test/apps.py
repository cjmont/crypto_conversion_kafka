from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TestConfig(AppConfig):
    name = "notbank.test"
    verbose_name = _("Test")

    def ready(self):
        try:
            import notbank.test.signals  # noqa F401
        except ImportError:
            pass
