# Generated by Django 5.0.1 on 2024-02-24 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('category', '0002_rename_category_categorymodel_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='category',
        ),
        migrations.AddField(
            model_name='books',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='category.categorymodel'),
        ),
    ]