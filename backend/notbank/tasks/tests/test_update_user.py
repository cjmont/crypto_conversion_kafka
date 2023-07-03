from uuid import uuid4

from django.test import TestCase
from notbank.base.utils.kafka.tramas.user_data import UserData
from notbank.base.utils.time import get_timestamp
from notbank.tasks.tasks.update_user import update_user
from notbank.transactions.models import User

SECONDS = 1


class SaveTransferTaskTest(TestCase):
    def setUp(self):
        self.user_uuid = uuid4()
        self.phone = '1231332'
        self.firebase_token = 'a token'
        self.user_data = UserData(
            uuid=str(self.user_uuid),
            timestamp=get_timestamp(),
            phone=self.phone,
            firebase_token=self.firebase_token,
        )

    def tearDown(self) -> None:
        try:
            User.objects.get(uuid=self.user_uuid).delete()
        except User.DoesNotExist:
            pass

    def test_update_user(self):
        update_user(self.user_data.to_trama())
        user = User.objects.get(uuid=self.user_uuid)
        self.assertEqual(user.uuid, self.user_uuid)
        self.assertEqual(user.phone, self.phone)
        self.assertEqual(user.firebase_token, self.firebase_token)

    def test_update_user_phone(self):
        update_user(self.user_data.to_trama())
        new_phone = '11111111'
        self.user_data.phone = new_phone
        update_user(self.user_data.to_trama())
        user = User.objects.get(uuid=self.user_uuid)
        self.assertEqual(user.phone, new_phone)

    def test_update_token(self):
        update_user(self.user_data.to_trama())
        new_token = 'a new token'
        self.user_data.firebase_token = new_token
        update_user(self.user_data.to_trama())
        user = User.objects.get(uuid=self.user_uuid)
        self.assertEqual(user.firebase_token, new_token)

    def test_update_all_but_uuid(self):
        self.user_data.phone = ''
        self.user_data.firebase_token = ''
        update_user(self.user_data.to_trama())
        user = User.objects.get(uuid=self.user_uuid)
        self.assertEqual(user.uuid, self.user_uuid)
        self.assertEqual(user.phone, None)
        self.assertEqual(user.firebase_token, None)
        new_token = 'a new token'
        self.user_data.firebase_token = new_token
        new_phone = '999999'
        self.user_data.phone = new_phone
        update_user(self.user_data.to_trama())
        user = User.objects.get(uuid=self.user_uuid)
        self.assertEqual(user.firebase_token, new_token)
        self.assertEqual(user.phone, new_phone)
