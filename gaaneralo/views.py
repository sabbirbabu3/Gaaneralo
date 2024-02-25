from django.shortcuts import render
from category.models import CategoryModel
from books.models import Books

def home(request, category_slug=None):
    data = Books.objects.all()
    if category_slug is not None:
        category = CategoryModel.objects.get(slug=category_slug)
        data = Books.objects.filter(category=category)
    categories = CategoryModel.objects.all()
    return render(request, 'home.html', {'data': data, 'category': categories})

