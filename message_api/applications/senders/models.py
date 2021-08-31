from django.db import models

OPERATION_OPTIONS = [
    ('debit', 'Debit'),
    ('credit', 'Credit')
]


class Sender(models.Model):
    user_id = models.PositiveIntegerField()
    user_name = models.CharField(max_length=150)
    user_email = models.EmailField(max_length=254, null=True)
    account = models.PositiveIntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    operation = models.CharField(max_length=6, choices=OPERATION_OPTIONS)
    message = models.CharField(max_length=150)
    when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Movement {self.id} - User: {self.user_name}'
