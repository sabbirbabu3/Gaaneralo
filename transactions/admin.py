from typing import Any
from django.contrib import admin
from .models import Transaction
# from .views import user_transaction_email
# Register your models here.

@admin.register(Transaction)

class TransactionAdmin(admin.ModelAdmin):
    list_display=['account','amount','balance_afet_transaction','transaction_type']