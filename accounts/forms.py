from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fields['username'].label = 'Create your Name'
        self.fields['email'].label = 'Give your Email Address'


class UpdateUserForm(ModelForm):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name')
        model = get_user_model()

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fields['username'].label = 'Update your username'
        self.fields['email'].label = 'Update your email'
