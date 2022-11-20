from django.urls import reverse

from rest_framework.test import APIClient, APITestCase

from .models import Balance


class APIFeatured(APITestCase):

    def setUp(self):
        self.client = APIClient()

        data = {
            "customer_xid": "ea0212d3-abd6-406f-8c67-868e814a2436"
        }
        response = self.client.post(reverse('auth_customer:auth_v1:init_wallet'), data=data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data.get("token"))

    def test_api_wallet(self):
        # test enabled
        response = self.client.post(reverse('wallet:wallet_api_v1:generic_wallet'))
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse('wallet:wallet_api_v1:generic_wallet'))
        self.assertEqual(response.status_code, 400)

        # test view
        response = self.client.get(reverse('wallet:wallet_api_v1:generic_wallet'))
        self.assertEqual(response.status_code, 200)

        # test top up
        data = {
            "amount": 100000,
            "reference_id":  "50535246-dcb2-4929-8cc9-004ea06f5241"
        }
        response = self.client.post(reverse('wallet:wallet_api_v1:top_up_wallet'), data=data)
        self.assertEqual(response.status_code, 201)
        balance = Balance.objects.last()
        self.assertEqual(100000, balance.amount)
        response = self.client.post(reverse('wallet:wallet_api_v1:top_up_wallet'), data=data)
        self.assertEqual(response.status_code, 400)
        data["reference_id"] = "12435246-dcb2-4929-8cc9-004ea06f5241"
        response = self.client.post(reverse('wallet:wallet_api_v1:top_up_wallet'), data=data)
        self.assertEqual(response.status_code, 201)
        balance = Balance.objects.last()
        self.assertEqual(200000, balance.amount)

        # test withdraw
        data = {
            "amount": 50000,
            "reference_id": "4b01c9bb-3acd-47dc-87db-d9ac483d20b2"
        }
        response = self.client.post(reverse('wallet:wallet_api_v1:withdraw_wallet'), data=data)
        self.assertEqual(response.status_code, 201)
        balance = Balance.objects.last()
        self.assertEqual(150000, balance.amount)
        response = self.client.post(reverse('wallet:wallet_api_v1:withdraw_wallet'), data=data)
        self.assertEqual(response.status_code, 400)
        data["reference_id"] = "1241c9bb-3acd-47dc-87db-d9ac483d20b2"
        response = self.client.post(reverse('wallet:wallet_api_v1:withdraw_wallet'), data=data)
        self.assertEqual(response.status_code, 201)
        balance = Balance.objects.last()
        self.assertEqual(100000, balance.amount)

        # test disabled
        data = {
            "is_disabled": True
        }
        response = self.client.patch(reverse('wallet:wallet_api_v1:generic_wallet'), data=data)
        self.assertEqual(response.status_code, 200)
        response = self.client.patch(reverse('wallet:wallet_api_v1:generic_wallet'), data=data)
        self.assertEqual(response.status_code, 400)

        response = self.client.get(reverse('wallet:wallet_api_v1:generic_wallet'))
        self.assertEqual(response.status_code, 404)
        data = {
            "amount": 50000,
            "reference_id": "4b01c9bb-3acd-47dc-87db-d9ac483d20b2"
        }
        response = self.client.post(reverse('wallet:wallet_api_v1:top_up_wallet'), data=data)
        self.assertEqual(response.status_code, 404)
        response = self.client.post(reverse('wallet:wallet_api_v1:withdraw_wallet'), data=data)
        self.assertEqual(response.status_code, 404)

        # test without token
        self.client.credentials()
        response = self.client.get(reverse('wallet:wallet_api_v1:generic_wallet'))
        self.assertEqual(response.status_code, 401)
        response = self.client.post(reverse('wallet:wallet_api_v1:generic_wallet'))
        self.assertEqual(response.status_code, 401)
        response = self.client.patch(reverse('wallet:wallet_api_v1:generic_wallet'))
        self.assertEqual(response.status_code, 401)
        response = self.client.post(reverse('wallet:wallet_api_v1:top_up_wallet'))
        self.assertEqual(response.status_code, 401)
        response = self.client.post(reverse('wallet:wallet_api_v1:withdraw_wallet'))
        self.assertEqual(response.status_code, 401)
