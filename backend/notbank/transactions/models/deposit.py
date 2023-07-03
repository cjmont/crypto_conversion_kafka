import uuid

from notbank.base.models.base import CommonModel
from django.db import models
from notbank.transactions.models.user import User

class Deposit(CommonModel):
    request_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user       = models.ForeignKey(User, on_delete=models.PROTECT)
    currency   = models.CharField(max_length=4)
    amount     = models.DecimalField(max_digits=36, decimal_places=18) 