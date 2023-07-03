import uuid

from notbank.base.models.base import CommonModel
from django.db import models


class CurrentDeposit(CommonModel):
    task_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    