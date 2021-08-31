from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from decimal import Decimal

from faker import Faker

from .models import FinancialAccount, MovementRegister
from applications.users.models import User

fake = Faker()


class AccountsValidationTestCase(TestCase):
    """This test case will be over the account fields validations rules."""

    def setUp(self):
        self.user = User.objects.create(
            username=fake.domain_word(),
            email=fake.email(),
            password=fake.password(),
            name=fake.name()
        )

    def test_account_fields_that_cant_be_blank(self):
        """A financial account should have a user associated as owner"""
        account = FinancialAccount()

        try:
            account.full_clean()
        except ValidationError as e:
            self.assertTrue('owner' in e.message_dict)

    def test_account_repr_format(self):
        """The representation of account should have be based on the
        owner name"""
        account = FinancialAccount.objects.create(owner=self.user)

        self.assertEqual(account.__repr__(),
                         f'<FinancialAccount: {self.user.name}>')

    def test_one_user_just_can_have_one_account(self):
        """The User only can have just a single account"""
        FinancialAccount.objects.create(owner=self.user)

        try:
            FinancialAccount.objects.create(owner=self.user)
        except IntegrityError as e:
            self.assertTrue('UNIQUE constraint failed' in e.args[0])

    def test_a_user_can_access_account_by_account_attr(self):
        """A User instance can access its account by user.account"""
        user = User.objects.create(
            username=fake.domain_word(), password=fake.password())
        FinancialAccount.objects.create(owner=user)

        self.assertTrue(user.account.owner.id == user.id)


class MovementRegisterValidationTestCase(TestCase):
    """This test case have movement register models validation fields
    as target"""

    def test_moviment_register_fields_cannot_be_blank(self):
        movement = MovementRegister()

        try:
            movement.full_clean()
        except ValidationError as e:
            self.assertTrue('account' in e.message_dict)
            self.assertTrue('who' in e.message_dict)
            self.assertTrue('movement_kind' in e.message_dict)


class FinancialAccountAndMovementRegisterEndpointsTestCase(TestCase):
    """This test case will check about the opening account, details of it
    and for the movements into it, by creating a new movement register for
    each transaction done."""

    def setUp(self):
        self.client = Client()

        self.password = fake.password()
        self.user = User.objects.create(
            username=fake.domain_word(),
            email=fake.email(),
            password=self.password,
            name=fake.name()
        )

        self.user.set_password(self.password)
        self.user.save()

        self.token = self.client.post('/authenticate', dict(
            username=self.user.username,
            password=self.password
        )).json()['token']

        self.header = f'Token {self.token}'

    def _account_creation_and_json_retrieval(self):
        """Account creation for authenticated user"""
        self.client.post(
            '/api/accounts/',
            {'owner': self.user.id},
            HTTP_AUTHORIZATION=self.header)

        response = self.client.get(
            '/api/accounts/', HTTP_AUTHORIZATION=self.header)

        return response

    def test_create_new_account(self):
        """When a post is submitted to /api/accounts by a token authenticated
        user, then a new account is created"""
        response = self._account_creation_and_json_retrieval()

        self.account = self.user.account

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.account.id == response.json()['id'])

    def test_authenticated_user_can_retrieve_its_own_account(self):
        """When a user do a GET /api/accounts/ then the account of this user
        is returned"""
        response = self._account_creation_and_json_retrieval()

        self.assertTrue(self.user.account.id == response.json()['id'])

    def test_credit_in_user_account(self):
        """The API have an endpoint to create some movements in account and
        the basic form is:

        {'operation': 'debit|credit', 'value': 0.0}
        """
        self._account_creation_and_json_retrieval()
        operation = {'operation': 'credit', 'value': '120'}

        response = self.client.post(
            '/api/accounts/movement',
            operation,
            HTTP_AUTHORIZATION=self.header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Decimal(response.json()['balance']), Decimal(120))

        operation['value'] = '200'

        response = self.client.post(
            '/api/accounts/movement',
            operation,
            HTTP_AUTHORIZATION=self.header)

        self.assertEqual(Decimal(response.json()['balance']), Decimal(320))

    def test_debit_in_user_account(self):
        """The API have an endpoint to create some movements in account and
        the basic form is:

        {'operation': 'debit|credit', 'value': 0.0}
        """
        self._account_creation_and_json_retrieval()
        account = self.user.account
        account.balance = Decimal(1000)
        account.save()

        response = self.client.post('/api/accounts/movement',
                                    {'operation': 'debit', 'value': 300},
                                    HTTP_AUTHORIZATION=self.header)

        self.assertEqual(Decimal(response.json()['balance']), Decimal(700))

        response = self.client.post('/api/accounts/movement',
                                    {'operation': 'debit', 'value': '900'},
                                    HTTP_AUTHORIZATION=self.header)

        self.assertEqual(Decimal(response.json()['account']['balance']),
                         Decimal(700))
        self.assertEqual(response.json()['message'], 'Not enough money')
