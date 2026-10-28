from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User
from users.enums import RoleChoices


# Create your forms here.

class CreateUserForm(UserCreationForm):
    first_name  = forms.CharField()
    last_name   = forms.CharField()
    
    class Meta:
        model   = User
        fields  = ['email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'status']


class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('email', 'password')
    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid login')


