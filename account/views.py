from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from  django.urls import reverse_lazy
# Create your views here.

class UserRegistrationView(FormView):
    template_name='registration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('register')

    def form_valid(self, form):
        user=form.save()
        login( self.request, user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name="login.html"
    def get_success_url(self):
        return reverse_lazy('profile')

def user_logout_view(request):
    logout(request)
    return redirect(reverse_lazy('home'))
def profile(request):
    return render(request, "profile.html")
    