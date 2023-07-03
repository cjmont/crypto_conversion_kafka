from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _

class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notbank.transactions'

    verbose_name = _("Transactions")

    def ready(self):
        try:
            import notbank.base.signals  # noqa F401
        except ImportError:
            pass

