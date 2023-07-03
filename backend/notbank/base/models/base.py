import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CommonModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Log(CommonModel):
    class LEVEL(models.IntegerChoices):
        ERROR = 0, _("ERROR")
        WARNING = 1, _("WARNING")
        INFO = 2, _("INFO")
        HTTP = 3, _("HTTP")
        DEBUG = 4, _("DEBUG")
    level = models.IntegerField(choices=LEVEL.choices)

    class SERVICE(models.TextChoices):
        SERVER = 'SERVER', _("SERVER")
        KAFKA_CONSUMER = 'KAFKA_CONSUMER', _("KAFKA CONSUMER")
        CELERY = 'CELERY', _("CELERY")
        KAFKA_PRODUCER = 'KAFKA_PRODUCER', _(
            "KAFKA PRODUCER (called from server or celery)")
        DELETE_OLD_QUOTE_CRON = 'DELETE_OLD_QUOTE_CRON', _("delete old quotes")
    service = models.TextField(choices=SERVICE.choices)

    message = models.TextField()

    def print(self):
        print(f'SERVICE   : {self.service}')
        print(f'LEVEL     : {self.LEVEL(self.level).name}')
        print(f'CREATED AT: {self.created_at}')
        for line in self.message.split('\n'):
            print(line)

    @staticmethod
    def create(level: int, message: str, service: str = SERVICE.SERVER):
        Log.objects.create(level=level, message=message, service=service)

    @staticmethod
    def error(message: str, service: str = SERVICE.SERVER):
        Log.objects.create(
            level=Log.LEVEL.ERROR,
            service=service,
            message=message,
        )

    @staticmethod
    def warning(message: str, service: str = SERVICE.SERVER):
        Log.objects.create(
            level=Log.LEVEL.WARNING,
            service=service,
            message=message,
        )

    @staticmethod
    def info(message: str, service: str = SERVICE.SERVER):
        Log.objects.create(
            level=Log.LEVEL.INFO,
            service=service,
            message=message,
        )

    @staticmethod
    def http(message: str, service: str = SERVICE.SERVER):
        Log.objects.create(
            level=Log.LEVEL.HTTP,
            service=service,
            message=message,
        )

    @staticmethod
    def debug(message: str, service: str = SERVICE.SERVER):
        Log.objects.create(
            level=Log.LEVEL.DEBUG,
            service=service,
            message=message,
        )
