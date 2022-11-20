from django.urls import reverse

from rest_framework.test import APIClient, APITestCase

from .models import CustomerAuth


class APIAuthCustomer(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_api_init(self):
        data = {
            "customer_xid": "ea0212d3-abd6-406f-8c67-868e814a2436"
        }

        response = self.client.post(reverse('auth_customer:auth_v1:init_wallet'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(0, CustomerAuth.objects.count())

        response = self.client.post(reverse('auth_customer:auth_v1:init_wallet'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["customer_xid"], CustomerAuth.objects.last().customer_xid)

        response = self.client.post(reverse('auth_customer:auth_v1:init_wallet'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(1, CustomerAuth.objects.count())
