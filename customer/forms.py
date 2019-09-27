from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    phonenumber=forms.CharField(max_length=16)

    class Meta:
        model=User
        fields=['username','email','phonenumber','password1','password2']


class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        '''
            update username and email
        '''
        model=User
        fields=['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_photo','phone_number',]        



