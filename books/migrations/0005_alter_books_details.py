# Generated by Django 5.0.1 on 2024-02-24 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_books_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='details',
            field=models.TextField(default='', null=True),
        ),
    ]
