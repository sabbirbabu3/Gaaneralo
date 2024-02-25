from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import ACCOUNT_TYPE, UserBankAccount

class UserRegistrationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'account_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            
            UserBankAccount.objects.create(
                user=user,
                account_type=account_type,
                account_no=100000 + user.id
            )
        return user
