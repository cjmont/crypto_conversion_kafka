
from django.db import models
from django.utils.translation import gettext_lazy as _
from notbank.base.models.base import CommonModel


class BMStatusWaitingSyncTask(CommonModel):
    task_id = models.CharField(max_length=300, unique=True)

    class STATUS(models.IntegerChoices):
        SUCCESS = 0, _("Éxito")
        ERROR = 1, _("Error")
        PENDING = 2, _("Pendiente")

    status = models.IntegerField(choices=STATUS.choices)
