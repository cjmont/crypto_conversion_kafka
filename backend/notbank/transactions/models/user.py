from notbank.base.models.base import CommonModel
from django.db import models


class User(CommonModel):
    phone = models.CharField(max_length=32, null=True)
    firebase_token = models.CharField(max_length=300, null=True)
