from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Key
    
class CreateUserForm(ModelForm):
    confirm_password = forms.CharField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'confirm_password',)
#        labels = {
#            'username' : _('Username:'),
#            'first_name' : _('First name:'),
#            'last_name' : _('Last name:'),
#            'email' : _('Email:'),
#            'password' : _('Enter password:'),
#        }
#        help_texts = {
#            'username' : _('This name will be visible when you make a post'),
#            'first_name' : _('JOHN doe'),
#            'last_name' : _('john DOE'),
#        }
#        widgets = {
#            'username' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Username'}),
#            'first_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'First name'}),
#            'last_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Last name'}),
#            'email' : forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'Email'}),
#            'password' : forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Password'}),
#        }

#407
class SecureKeyForm(ModelForm):
    password = forms.CharField()
    confirm_digit = forms.CharField()
    class Meta:
        model = Key
        fields = ('digit', 'start', 'end','confirm_digit','password',)
        
class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username' : _('Username'),
            'password' : _('Password'),
        }