# Generated by Django 5.0.1 on 2024-02-24 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_remove_books_description_books_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='details',
            field=models.TextField(default=True),
        ),
    ]
