import uuid

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from apps.auth_customer.models import CustomerAuth
from .signals import update_balance


class Balance(models.Model):

    class StatusChoices(models.IntegerChoices):
        DISABLED = 0, _('Disabled')
        ENABLED = 1, _('Enabled')

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    customer = models.OneToOneField(CustomerAuth, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default=0)
    status = models.SmallIntegerField(choices=StatusChoices.choices, default=StatusChoices.DISABLED)
    update_status_at = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    STATUS_CHOICES = (
        (0, 'Failed'),
        (1, 'Success'),
        (2, 'Pending'),
    )
    TYPE_CHOICES = (
        (0, 'Withdraw'),
        (1, 'Top Up'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    type = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    ref_id = models.CharField(max_length=50)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('type', 'ref_id',)


post_save.connect(update_balance, Transaction)
