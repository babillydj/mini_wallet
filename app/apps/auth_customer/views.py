from secrets import token_hex

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import CustomerAuth


@api_view(['POST'])
@permission_classes((AllowAny, ))
def init_wallet(request):
    data = request.data
    if data.get("customer_xid"):
        customer, created = CustomerAuth.objects.get_or_create(
            customer_xid=data.get("customer_xid"),
            defaults={"token": token_hex(21)}
        )
        return Response({"token": customer.token}, status=status.HTTP_201_CREATED)

    return Response({"message": "no customer_xid provided"}, status=status.HTTP_400_BAD_REQUEST)
