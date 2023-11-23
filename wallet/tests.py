import pytest
from django.contrib.auth.models import User

from .models import Wallet, Transaction

pytestmark = pytest.mark.django_db


def test_wallet_create():
    admin = User.objects.create(username="admin")
    wallet = Wallet.objects.create(
        user_id=admin,
        currency="RUB",
        amount=100,
    )
    wallets = Wallet.objects.all()
    transaction = Transaction.objects.filter(wallet=wallet)
    assert wallets.count() == 1
    assert wallet.user_id == admin
    assert wallet.currency == "RUB"
    assert wallet.amount == 100
    assert transaction.count() == 1


def test_multiple_wallets():
    admin = User.objects.create(username="admin")
    wallet_rub = Wallet.objects.create(
        user_id=admin,
        currency="RUB",
        amount=100,
    )
    wallet_usd = Wallet.objects.create(
        user_id=admin,
        currency="USD",
        amount=200,
    )
    wallets = Wallet.objects.all()
    assert wallets.count() == 2


def test_multiple_user():
    admin = User.objects.create(username="admin")
    user = User.objects.create(username="user")
    wallet_admin = Wallet.objects.create(
        user_id=admin,
        currency="RUB",
        amount=100,
    )
    wallet_user = Wallet.objects.create(
        user_id=user,
        currency="USD",
        amount=200,
    )
    wallets = Wallet.objects.all()
    assert wallets.count() == 2
