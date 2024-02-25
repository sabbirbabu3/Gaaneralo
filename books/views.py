from django.shortcuts import redirect, render
from django.views.generic import DetailView
from . import models
from . import forms
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect


# Create your views here.
class CardetailsView(DetailView):
    model = models.Books
    template_name = 'details.html'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        form = forms.CommentsForm(request.POST)
        if form.is_valid():
            book = self.get_object()
            new_comment = form.save(commit=False)
            new_comment.car_model = book
            new_comment.save()
            return redirect('details', id=book.id)
        else:
            # If form is not valid, re-render the details page with the form and existing comments
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carmodel = self.object
        comments = models.comments.objects.filter(car_model=carmodel)
        form = forms.CommentsForm()
        context['comments'] = comments
        context['comments_form'] = form
        return context