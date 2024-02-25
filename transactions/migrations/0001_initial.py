# Generated by Django 5.0.1 on 2024-02-24 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_alter_userbankaccount_account_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('balance_afet_transaction', models.DecimalField(decimal_places=2, max_digits=12)),
                ('transaction_type', models.IntegerField(choices=[(1, 'deposite'), (2, 'Bybook'), (3, 'Loan'), (4, 'loan paid')], null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('loan_approve', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='account.userbankaccount')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
