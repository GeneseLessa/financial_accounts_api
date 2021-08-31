from django.db import models
from django.contrib.auth.models import User as BaseUser

KINDS = [
    ('a', 'Admin'),
    ('c', 'Common')
]


class User(BaseUser):
    """This model is responsible for user authentication and base creation
    for many kind of users in the system.

    Args:
        BaseUser (AbstractUser): personalized user for Accounts API
    """
    name = models.CharField(max_length=150, verbose_name='Nome')
    kind = models.CharField(max_length=50, choices=KINDS, default='c')

    def __str__(self):
        return self.name
