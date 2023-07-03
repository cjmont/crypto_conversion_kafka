import unittest
from notbank.base.utils.kafka.authentication import sign
from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException, TramaValidationException
from notbank.base.utils.kafka.tramas.user_data import UserData


class UserDataTestCase(unittest.TestCase):
    trama_data: str
    timestamp: str  # 13
    uuid: str  # 36
    phone: str  # 32
    firebase_token: str  # 255, optional

    def setUp(self):
        self.timestamp = "1652981386000".rjust(13, ' ')
        self.uuid = "1e9bb042-6789-4183-8587-4d40ab130b85".rjust(36, ' ')
        self.phone = "11019239420".rjust(32, ' ')
        self.firebase_token = "as-daosdasf-a14-3r-asdofggfde-w89gsug0a13-fgasdoau023rvaef20a-sdf-awocw3v3".rjust(
            255, ' ')
        self.trama_data = ''.join([
            self.timestamp,
            self.uuid,
            self.phone,
            self.firebase_token,
        ])

    def test_read_from_trama(self):
        trama = self.trama_data + sign(self.trama_data)
        user_data = UserData.from_trama(trama)

        self.assertEqual(self.timestamp.lstrip(), user_data.timestamp)
        self.assertEqual(self.uuid.lstrip(), user_data.uuid)
        self.assertEqual(self.phone.lstrip(), user_data.phone)
        self.assertEqual(
            self.firebase_token.lstrip(),
            user_data.firebase_token
        )

    def test_read_from_invalid_trama(self):
        # ! less than 32 characters => fails
        phone_number = "123123123"
        trama_data = ''.join([
            self.timestamp,
            self.uuid,
            phone_number,
            self.firebase_token,
        ])
        trama = trama_data + sign(trama_data)
        self.assertRaises(
            TramaFormatException,
            UserData.from_trama,
            trama,
        )

    def test_read_from_badly_signed_trama(self):
        # ! corrupting signature
        trama = self.trama_data + sign(self.trama_data)[:-1] + 'l'
        self.assertRaises(
            TramaValidationException,
            UserData.from_trama,
            trama,
        )

if __name__ == '__main__':
    unittest.main()
