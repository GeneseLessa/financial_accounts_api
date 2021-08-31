from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from faker import Faker

from .models import User

fake = Faker()


class UserValidationsTestCase(TestCase):
    """This test case checks for all the validations in the user model"""

    def setUp(self):
        User.objects.create(
            username=fake.domain_word(),
            email=fake.email(),
            password=fake.password())

    def test_representational_string_of_user_object(self):
        """Should have the same representational string into ORM and
        json endpoint response"""
        user = User.objects.first()
        self.assertEqual(user.__repr__(), f'<User: {user.name}>')

    def test_user_fields_that_cant_be_blank(self):
        """Checking the obligatoriness of some fields"""
        u = User()

        try:
            u.full_clean()
        except ValidationError as e:
            self.assertTrue('name' in e.message_dict)
            self.assertTrue('username' in e.message_dict)
            self.assertTrue('password' in e.message_dict)

    def test_cant_create_two_users_with_same_username(self):
        """Should failed if two users with same username is trying to be
        created"""
        username = fake.domain_word()

        try:
            for i in range(0, 2):
                User.objects.create(
                    username=username,
                    email=fake.email(),
                    password=fake.password())

        except IntegrityError as e:
            self.assertTrue('UNIQUE constraint failed' in e.args[0])

    def test_cant_create_two_users_with_same_email(self):
        """Should failed if two users with same email is trying to be
        created"""
        email = fake.email()

        try:
            for i in range(0, 2):
                User.objects.create(
                    username=fake.domain_word(),
                    email=email,
                    password=fake.password())

        except IntegrityError as e:
            self.assertTrue('UNIQUE constraint failed' in e.args[0])


class UserEndpointsTestCase(TestCase):
    """This testcase will use django test client for checking for the good
    work of endpoints in the API."""

    def setUp(self):
        self.client = Client()
        self.password = fake.password()

        self.user = User.objects.create(
            username=fake.domain_word(),
            password=self.password,
            email=fake.email(),
            name=fake.name()
        )
        self.user.set_password(self.password)
        self.user.save()

    def test_user_created_by_endpoint(self):
        """Creation of a user through POST at /api/users/create_user"""
        users = User.objects.all()
        initial_size = len(users)

        response = self.client.post('/api/users/create_user', dict(
            name=fake.name(),
            email=fake.email(),
            username=fake.domain_word(),
            password=fake.password()
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(initial_size < len(User.objects.all()))

    def test_list_all_users_when_dont_pass_an_id(self):
        """The endpoint /api/users/ should get all system users when don't
        pass a valid id as the last parameter of the route"""

        for i in range(0, 11):
            User.objects.create(
                username=fake.domain_word(),
                email=fake.email(),
                password=fake.password(),
                name=fake.name())

        response = self.client.get('/api/users/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), len(User.objects.all()))

    def test_details_user_when_show_the_id_in_the_route(self):
        """This route can show the user details when id is informed"""

        user = User.objects.first()
        response = self.client.get(f'/api/users/{user.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.id, response.json()['id'])

    def test_password_of_a_new_user_should_be_encrypted(self):
        """When a new user is created, the password should be diferent of
        initial password state (not encrypted)"""
        password = fake.password()
        response = self.client.post('/api/users/create_user', dict(
            username=fake.domain_word(),
            name=fake.name(),
            email=fake.email(),
            password=password
        ))

        self.assertFalse(password == response.json()['password'])

    def test_authentication_enpoint(self):
        """Passing a valid username and password for the authentication
        endpoint, the API should return a token for authorizing access
        or a error when credentials are invalid"""

        response = self.client.post('/authenticate', dict(
            username=self.user.username,
            password=self.password
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.json())
