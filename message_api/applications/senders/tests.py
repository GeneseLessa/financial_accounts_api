from django.test import TestCase, Client
from django.core.exceptions import ValidationError
# from django.db.utils import IntegrityError
from faker import Faker

from .models import Sender

fake = Faker()


class SenderValidationTestCase(TestCase):
    """This test case check the model validation"""

    def setUp(self):
        self.sender = Sender(
            user_id=1,
            user_name=fake.domain_word(),
            user_email=fake.email(),
            account=1,
            value=round(120.00),
            operation='debt',
            message=fake.text()[0:100]
        )

    def test_validation_fields(self):
        sender = Sender()
        fields = 'user_id user_name user_email account value operation message'

        try:
            sender.full_clean()
        except ValidationError as e:
            fields = [x for x in fields.split()]

            for i in fields:
                self.assertTrue(i in e.message_dict)

    def test_operations_only_can_be_debit_or_credit(self):
        """Only debt or credit can be choosen as operation"""
        self.sender.operation = 'other'

        try:
            self.sender.full_clean()
        except ValidationError as e:
            self.assertTrue(
                'is not a valid choice' in e.message_dict['operation'][0])

        self.sender.operation = 'credit'

        self.assertTrue(self.sender.full_clean() is None)


class EndpointsTestCase(TestCase):
    """This test case targets the base endpoint to setup mail send and
    register the event through the send model."""

    def setUp(self):
        self.client = Client()
        self.sender = dict(
            user_id=1,
            user_name=fake.domain_word(),
            user_email='genese.lessa@gmail.com',
            account=1,
            value=round(120.00),
            operation='debit',
            message=fake.text()[0:100]
        )

    def test_post_in_specific_endpoint(self):
        """Only check the endpoint availability"""
        response = self.client.post('/sender')
        self.assertEqual(response.status_code, 200)

    def test_creation_of_send_register_through_endpoint(self):
        """Send a complete register of a movement in API and pass it to
        endpoint, then expect to create a new register of sender model"""
        initial_size = len(Sender.objects.all())

        response = self.client.post('/sender', self.sender)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(initial_size < len(Sender.objects.all()))
