from django import forms
from .models import Books,comments

class BooksForm(forms.ModelForm):
    class Meta:
        model=Books
        fields="__all__"

class CommentsForm(forms.ModelForm):
    class Meta:
        model=comments
        exclude = ['car_model'] 