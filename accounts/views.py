from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from . import forms
from .models import User
from django.contrib.auth import get_user_model
from django.contrib import messages


# Create your views here.


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'


class UserUpdateView(UpdateView):
    model = get_user_model()
    template_name = 'accounts/update-profile.html'
    form_class = forms.UpdateUserForm

    def get_success_url(self):
        messages.success(self.request, 'Your profile has been updated.')
        return str(reverse_lazy('accounts:profile', kwargs=self.kwargs))
