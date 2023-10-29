from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LogoutView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


# class LoggedOut(LogoutView):
#     form_class
#     success_url = reverse_lazy('posts:index')
#     template_name = 'users/signup.html'
