from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import exceptions

from apps.auth_customer.models import CustomerAuth


class CustomAuthentication(TokenAuthentication):
    model = CustomerAuth

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            customer = model.objects.get(token=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        return customer, None


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CsrfExemptTokenAuthentication(CustomAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
