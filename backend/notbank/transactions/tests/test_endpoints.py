import json
import unittest
from unittest.mock import patch
from django.conf import settings

from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate


from notbank.base.utils.kafka.producer import Producer
from notbank.transactions.models import User
from django.contrib.auth.models import User as DjangoUser

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


@patch.object(Producer, 'send_kafka_message')
class ServicesTestCase(unittest.TestCase):
    def setUp(self):
        self.user_data = {'username': '583e87c9-871a-404d-810d-3aa124661e65', 'password': 'secretos'}
        self.test_user = DjangoUser(
            **self.user_data,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        self.test_user.save()
        for attr, value in self.test_user.__dict__.items():
            print((attr, value))
        print('---------')
        self.user_1 = User(uuid='583e87c9-871a-404d-810d-3aa124661e65')
        self.user_1.save()
        self.user_2 = User()
        self.user_2.save()
        self.client = APIClient(enforce_csrf_checks=True)
        # self.client.login(**self.user_data)

        self.factory = APIRequestFactory()

    def tearDown(self):
        User.objects.all().delete()
        try:
            self.test_user.delete()
        except:
            pass

    def test_pay_to_user(self, mock_send_kafka_message):
        # response = self.client.post(
        #     '/api/token/',
        #     json.dumps(self.user_data),
        #     content_type='application/json')
        try:
            token_request = self.factory.post(
                '/api/token/',
                json.dumps({
                    'username': '583e87c9-871a-404d-810d-3aa124661e65',
                    'password': 'secretos'
                }),
                content_type='application/json'
            )
            # force_authenticate(token_request, user=self.test_user)
            token_view = TokenObtainPairView.as_view()
            response = token_view(token_request)
            print(response)
        except Exception as e:
            print(e)
        try:
            print(response.data)
        except Exception as e:
            print(e)

        # data = {
        #     'to_user': str(self.user_2.uuid),
        #     'currency': 'EOS',
        #     'amount': '30.3',
        #     'fee_amount': '2',
        #     'description': 'a pay to a user'
        # }
        # request = self.factory.post(
        #     '/transactions/paytouser',
        #     json.dumps(data),
        #     content_type='application/json')
        # # force_authenticate(request, user=self.user)
        # view = PayToUserView.as_view()
        # response = view(request)
        # print(response)
