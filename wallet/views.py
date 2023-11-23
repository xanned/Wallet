import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from wallet.models import Wallet, Transaction

logger = logging.getLogger(__name__)


def change_balance(transaction_data, wallet_action):
    queryset = Wallet.objects.all()
    wallet_id = transaction_data.get("wallet_id")
    if type(wallet_id) is not int:
        return Response({"error": "Wallet ID incorrect"}, status=400)
    deposit_wallet = queryset.filter(pk=wallet_id)
    if deposit_wallet.count() != 1:
        return Response({"error": "Wallet ID not found"}, status=400)
    amount = transaction_data.get("amount", 0)
    if type(amount) not in (int, float) or amount <= 0:
        return Response({"error": "Incorrect amount"}, status=400)
    wallet = deposit_wallet.get()
    currency = transaction_data.get("currency")
    response = {}
    action = 0
    if currency != wallet.currency:
        return Response({"error": "Incorrect currency"}, status=400)
    if wallet_action == "Deposit":
        wallet.amount += amount
        wallet.save()
        action = 2
        response = {"success": f"Deposited {amount} {wallet.currency} to wallet #{wallet.id}"}
    elif wallet_action == "Withdrawal":
        if amount > wallet.amount:
            return Response({"error": "Incorrect amount"}, status=400)
        wallet.amount -= amount
        wallet.save()
        action = 4
        response = {"success": f"Withdrawn {amount} {wallet.currency} from wallet #{wallet.id}"}
    else:
        return Response(response, status=400)
    transaction = Transaction.objects.create(wallet=wallet, action=action, amount=amount)
    transaction.save()
    logger.info(f"Transaction for wallet #{transaction.wallet.id}")
    return Response(response, status=200)


class WalletDeposit(APIView):

    def post(self, request):
        transaction_data = request.data
        return change_balance(transaction_data, "Deposit")


class WalletWithdrawal(APIView):

    def post(self, request):
        transaction_data = request.data
        return change_balance(transaction_data, "Withdrawal")


class WallerTransfer(APIView):

    def post(self, request):
        queryset = Wallet.objects.all()
        transaction_data = request.data
        from_wallet_id = transaction_data.get("from_wallet")
        to_wallet_id = transaction_data.get("to_wallet")
        amount = transaction_data.get("amount")
        currency = transaction_data.get("currency")
        if type(amount) not in (int, float) or amount <= 0:
            return Response({"error": "Incorrect amount"}, status=400)
        if type(from_wallet_id) is not int or type(to_wallet_id) is not int:
            return Response({"error": "Wallet ID incorrect"}, status=400)
        from_wallet = queryset.filter(pk=from_wallet_id)
        to_wallet = queryset.filter(pk=to_wallet_id)
        if from_wallet.count() != 1 or to_wallet.count() != 1:
            return Response({"error": "Wallet ID not found"}, status=400)
        from_wallet_obj = from_wallet.get()
        to_wallet_obj = to_wallet.get()
        if currency != from_wallet_obj.currency or currency != to_wallet_obj.currency:
            return Response({"error": "Incorrect currency"}, status=400)
        if amount > from_wallet_obj.amount:
            return Response({"error": "Incorrect amount"}, status=400)
        from_wallet_obj.amount -= amount
        from_wallet_obj.save()
        to_wallet_obj.amount += amount
        to_wallet_obj.save()
        transaction = Transaction.objects.create(wallet=from_wallet_obj, amount=amount, transfer_wallet=to_wallet_obj,
                                                 action=3)
        transaction.save()
        logger.info(
            f"Transfer transaction from wallet #{transaction.wallet.id} to wallet #{transaction.transfer_wallet.id}")
        return Response({
            "success": f"Transferred {amount} {currency} to wallet #{to_wallet_obj.id} from wallet #{from_wallet_obj.id}"})

