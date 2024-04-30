from socket import fromshare
from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from blog.models import Post


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'style': 'background:gray'}))
    password2 = forms.CharField(label="Confirma tu Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'style': 'background:gray'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'first_name': 'Nombre',
                  'last_name': 'Apellido', 'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'style': 'background:gray'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'background:gray'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'background:gray'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'background:gray'})
                   }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'desc']
        labels = {'title': 'Título', 'desc': 'Contenido'}
        widgets = {'title': forms.TextInput(
            attrs={'class': 'form-control'}), 'desc': forms.Textarea(attrs={'class': 'form-control'})}
