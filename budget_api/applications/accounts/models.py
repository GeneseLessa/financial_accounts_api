from django.db import models

from applications.users.models import User

ACCOUNT_KIND = [
    ('pf', u'Pessoa física'),
    ('pj', u'Pessoa jurídica')
]


class FinancialAccount(models.Model):
    """This model have the basic account structure for transactions and
    basic financial registers"""
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='account')
    kind = models.CharField(max_length=2, choices=ACCOUNT_KIND, default='pf')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.owner.name


MOVEMENT_KINDS = [
    ('debit', u'Débito'),
    ('credit', u'Crédito')
]


class MovementRegister(models.Model):
    account = models.ForeignKey(
        FinancialAccount, on_delete=models.CASCADE, related_name='movements')
    when = models.DateTimeField(auto_now_add=True)
    who = models.ForeignKey(User, on_delete=models.SET_NULL,
                            null=True, related_name='movements_i_did')
    movement_kind = models.CharField(max_length=6, choices=MOVEMENT_KINDS)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.account} - {self.movement_kind}'
