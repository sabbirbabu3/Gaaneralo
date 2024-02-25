# Generated by Django 5.0.1 on 2024-02-24 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_books_details'),
        ('category', '0002_rename_category_categorymodel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='category',
            field=models.ManyToManyField(to='category.categorymodel'),
        ),
        migrations.AlterField(
            model_name='books',
            name='details',
            field=models.TextField(default=''),
        ),
    ]