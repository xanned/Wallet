import json

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .models import Wallet

pytestmark = pytest.mark.django_db
client = APIClient()


def test_deposit():
    request = client.post("/deposit", json.dumps({"wallet_id": 1, "currency": "RUB", "amount": 10}),
                          content_type="application/json")
    assert request.status_code == 400
    assert request.data == {"error": "Wallet ID not found"}
    initial_amount = 1000
    amount = 100
    currency = "RUB"
    admin = User.objects.create(username="admin")
    wallet = Wallet.objects.create(
        user_id=admin,
        currency=currency,
        amount=initial_amount,
    )
    request = client.post("/deposit", json.dumps({"wallet_id": wallet.id, "currency": currency, "amount": amount}),
                          content_type="application/json")
    assert request.status_code == 200
    assert request.data == {'success': f'Deposited {amount} {wallet.currency} to wallet #{wallet.id}'}
    wallet = Wallet.objects.get(user_id=admin)
    assert wallet.amount == initial_amount + amount

    request = client.post("/deposit", json.dumps({"wallet_id": wallet.id, "currency": "USD", "amount": amount}),
                          content_type="application/json")
    assert request.status_code == 400
    assert request.data == {'error': 'Incorrect currency'}

    request = client.post("/deposit", json.dumps({"wallet_id": wallet.id, "currency": "USD", "amount": -1}),
                          content_type="application/json")
    assert request.status_code == 400
    assert request.data == {'error': "Incorrect amount"}


def test_withdrawal():
    request = client.post("/withdrawal", json.dumps({"wallet_id": 1, "currency": "RUB", "amount": 10}),
                          content_type="application/json")
    assert request.status_code == 400
    assert request.data == {"error": "Wallet ID not found"}
    initial_amount = 1000
    amount = 100
    currency = "RUB"
    admin = User.objects.create(username="admin")
    wallet = Wallet.objects.create(
        user_id=admin,
        currency=currency,
        amount=initial_amount,
    )
    request = client.post("/withdrawal", json.dumps({"wallet_id": wallet.id, "currency": currency, "amount": amount}),
                          content_type="application/json")
    assert request.status_code == 200
    assert request.data == {'success': f'Withdrawn {amount} {wallet.currency} from wallet #{wallet.id}'}
    wallet = Wallet.objects.get(user_id=admin)
    assert wallet.amount == initial_amount - amount

    request = client.post("/withdrawal", json.dumps({"wallet_id": wallet.id, "currency": "USD", "amount": amount}),
                          content_type="application/json")
    assert request.status_code == 400
    assert request.data == {'error': 'Incorrect currency'}

    request = client.post("/withdrawal", json.dumps({"wallet_id": wallet.id, "currency": currency, "amount": 10000}),
                          content_type="application/json")
    assert request.status_code == 400
    assert request.data == {'error': 'Incorrect amount'}


def test_transfer():
    initial_amount = 1000
    amount = 100
    currency = "RUB"

    admin = User.objects.create(username="admin")
    wallet_admin = Wallet.objects.create(
        user_id=admin,
        currency=currency,
        amount=initial_amount,
    )

    user = User.objects.create(username="user")
    wallet_user = Wallet.objects.create(
        user_id=user,
        currency=currency,
        amount=initial_amount,
    )

    request = client.post("/transfer",
                          json.dumps({"from_wallet": wallet_admin.id, "currency": currency, "amount": amount,
                                      "to_wallet": wallet_user.id}),
                          content_type="application/json")
    assert request.status_code == 200
    assert request.data == {
        'success': f'Transferred {amount} {currency} to wallet #{wallet_user.id} from wallet #{wallet_admin.id}'}

    wallet_admin = Wallet.objects.get(user_id=admin)
    wallet_user = Wallet.objects.get(user_id=user)
    assert wallet_admin.amount == initial_amount - amount
    assert wallet_user.amount == initial_amount + amount

    request = client.post("/transfer",
                          json.dumps({"from_wallet": wallet_admin.id, "currency": "USD", "amount": amount,
                                      "to_wallet": wallet_user.id}),
                          content_type="application/json")
    assert request.status_code == 400
    assert request.data == {'error': 'Incorrect currency'}

    request = client.post("/transfer",
                          json.dumps({"from_wallet": wallet_admin.id, "currency": currency, "amount": 10000,
                                      "to_wallet": wallet_user.id}),
                          content_type="application/json")
    assert request.status_code == 400
    assert request.data == {'error': 'Incorrect amount'}
