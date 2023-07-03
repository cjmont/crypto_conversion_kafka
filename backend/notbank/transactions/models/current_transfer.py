import uuid

from notbank.base.models.base import CommonModel
from django.db import models


class CurrentTransfer(CommonModel):
    task_id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)