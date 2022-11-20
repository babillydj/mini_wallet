from rest_framework import serializers

from .models import Balance, Transaction


class TransactionUpdateSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    reference_id = serializers.CharField()


class WalletDisabledSerializer(serializers.Serializer):
    is_disabled = serializers.BooleanField()


class WalletSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid")
    balance = serializers.IntegerField(source="amount")
    status = serializers.SerializerMethodField()
    owned_by = serializers.CharField(source="customer.customer_xid")

    class Meta:
        model = Balance
        fields = ["id", "owned_by", "status", "balance"]

    @staticmethod
    def get_status(obj):
        return obj.get_status_display()


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid")
    reference_id = serializers.CharField(source="ref_id")
    status = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ["id", "status", "amount", "reference_id"]

    @staticmethod
    def get_status(obj):
        return obj.get_status_display()
