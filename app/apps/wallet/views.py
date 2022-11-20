from datetime import datetime

from django.db import IntegrityError, transaction as tr
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from core.base import BaseResponse
from .models import Balance, Transaction
from .serializers import (TransactionUpdateSerializer, TransactionSerializer, WalletDisabledSerializer,
                          WalletSerializer)


class Wallet(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        balance = get_object_or_404(Balance, customer=request.user, status=1)
        serializer = WalletSerializer(balance)
        data = serializer.data
        data["enabled_at"] = balance.update_status_at
        res = {"wallet": data}
        return BaseResponse(res, status=status.HTTP_200_OK)

    def post(self, request):
        balance = get_object_or_404(Balance, customer=request.user)
        if balance.status != 0:
            return BaseResponse(message="wallet already enabled", status=status.HTTP_400_BAD_REQUEST)
        balance.status = 1
        balance.update_status_at = datetime.now()
        balance.save()

        serializer = WalletSerializer(balance)
        data = serializer.data
        data["enabled_at"] = balance.update_status_at

        res = {"wallet": data}
        return BaseResponse(res, status=status.HTTP_201_CREATED)

    def patch(self, request):
        serializer = WalletDisabledSerializer(data=request.data)
        if serializer.is_valid():
            balance = get_object_or_404(Balance, customer=request.user)
            if balance.status != 1:
                return BaseResponse(message="wallet already disabled", status=status.HTTP_400_BAD_REQUEST)
            balance.status = 0
            balance.update_status_at = datetime.now()
            balance.save()

            serializer = WalletSerializer(balance)
            data = serializer.data
            data["disabled_at"] = balance.update_status_at
            data = {"wallet": data}
            return BaseResponse(data, status=status.HTTP_200_OK)

        return BaseResponse(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def top_up(request):
    customer = request.user
    serializer = TransactionUpdateSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        balance = get_object_or_404(Balance, customer=customer, status=1)

        try:
            with tr.atomic():
                transaction = Transaction.objects.create(
                    balance=balance,
                    date=datetime.now(),
                    amount=data.get("amount"),
                    type=1,
                    status=1,
                    ref_id=data.get("reference_id")
                )
                serializer = TransactionSerializer(transaction)
                data = serializer.data
                data["deposited_by"] = customer.customer_xid
                data["deposited_at"] = transaction.date
                res = {"deposit": data}
                return BaseResponse(res, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(e.__cause__)
            return BaseResponse(message="bad request data", status=status.HTTP_400_BAD_REQUEST)

    return BaseResponse(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def withdraw(request):
    customer = request.user
    serializer = TransactionUpdateSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        balance = get_object_or_404(Balance, customer=customer, status=1)
        if balance.amount < data.get("amount"):
            return BaseResponse(message="withdrawal amount is bigger than balance", status=status.HTTP_400_BAD_REQUEST)

        try:
            with tr.atomic():
                transaction = Transaction.objects.create(
                    balance=balance,
                    date=datetime.now(),
                    amount=data.get("amount"),
                    type=0,
                    status=1,
                    ref_id=data.get("reference_id")
                )
                serializer = TransactionSerializer(transaction)
                data = serializer.data
                data["withdrawn_by"] = customer.customer_xid
                data["withdrawn_at"] = transaction.date
                res = {"withdrawal": data}
                return BaseResponse(res, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(e.__cause__)
            return BaseResponse(message="bad request data", status=status.HTTP_400_BAD_REQUEST)

    return BaseResponse(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
