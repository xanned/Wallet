import logging
import time
import uuid

from django.contrib.auth.models import User
from django.db import models

logger = logging.getLogger(__name__)


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, models.CASCADE)
    RUB = "RUB"
    USB = "USD"
    CURRENCY_CHOICES = [
        (RUB, "Russian rubles"),
        (USB, "US dollars")
    ]
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=RUB)
    amount = models.FloatField(default=1000.0)

    def username(self):
        return self.user_id.username

    def __str__(self):
        return f'Wallet in {self.currency},  id #{self.id}'

    def save(self, *args, **kwargs):
        is_create = False
        if self.id is None:
            is_create = True
        super().save(*args, **kwargs)
        if is_create:
            create_transaction = Transaction(uuid=uuid.uuid4(), amount=self.amount, wallet=self, datetime=time.time(),
                                             action=1)
            create_transaction.save()
            logger.info(f"Wallet for {self.user_id.username} created")


class Transaction(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    datetime = models.DateTimeField(auto_now_add=True)
    wallet = models.ForeignKey(Wallet, models.CASCADE)
    ACTION_CHOICES = [
        (1, "Create"),
        (2, "Deposit"),
        (3, "Transfer"),
        (4, "Withdrawal"),
    ]
    action = models.IntegerField(choices=ACTION_CHOICES)
    transfer_wallet = models.ForeignKey(Wallet, models.CASCADE, null=True, blank=True, related_name="transfer")
    amount = models.FloatField()

    def __str__(self):
        return f'Wallet {self.wallet.user_id.username} transaction, uuid: {self.uuid}'
