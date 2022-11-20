from django.http import HttpResponseForbidden

from rest_framework import permissions

from .models import CustomerAuth


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.headers.get("Authorization"):
            token = request.headers.get("Authorization").split(" ")[1]
            customer = CustomerAuth.objects.filter(token=token)
            if customer.exists():
                request["customer"] = customer
                return True

        return False
