from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ACCOUNT_TYPE = (
    ('DEPOSIT', 'Deposit'),
    ('BYBOOK', 'bybook'),
)

class UserBankAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE)
    account_no = models.IntegerField(unique=True)
    balance = models.DecimalField(max_digits=12, default=0, decimal_places=2)

    def __str__(self):
        return str(self.account_no)
