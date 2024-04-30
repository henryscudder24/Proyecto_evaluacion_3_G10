from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
import requests
import os
from requests.exceptions import RequestException
# Home


def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

# Acerca de


def about(request):
    return render(request, 'blog/about.html')

# Contacto


def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'fname': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login/')

# Logout


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Signup


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Autor')
            user.groups.add(group)
            # Agregar token * Validar FS
            Token.objects.create(user=user)
            messages.success(request, 'Muchas gracias por tu aporte.')
            return HttpResponseRedirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

# Login


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    Token.objects.get_or_create(user=user)
                    messages.success(request, 'Inicio de sesión exitoso')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')

# Agregar post / FS


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

# recordar dirigir las url de miniblog en el main
# acciones para los post /Fabian Solar


def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

# Delete New Post


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')


def book_viewer(request):
    return render(request, 'blog/books.html')


def chatgpt_view(request):
    user_input = request.GET.get('prompt', '')
    if user_input:
        headers = {
            'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}'
        }
        data = {
            'messages': [{'role': 'user', 'content': user_input}],
            'model': 'gpt-3.5-turbo',
            'temperature': 0.5,
            'max_tokens': 150
        }
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions', json=data, headers=headers)
            response_data = response.json()
            print("Response from OpenAI:", response_data)
            return JsonResponse(response_data)
        except RequestException as e:
            print("An error occurred: ", str(e))
            return JsonResponse({'error': 'Failed to communicate with OpenAI API'}, status=500)
    return render(request, 'blog/chatgpt.html')
