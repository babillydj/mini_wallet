from django.db import models
from django.db.models.signals import post_save

from .signals import create_wallet


class CustomerAuth(models.Model):
    customer_xid = models.CharField(max_length=50)
    token = models.CharField(max_length=50)
    is_authenticated = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


post_save.connect(create_wallet, CustomerAuth)
