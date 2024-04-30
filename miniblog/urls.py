
from django.contrib import admin
from django.urls import path, include
from blog import views
import requests
from rest_api.viewsLogin import login
from blog.views import book_viewer
from django.contrib import admin
from blog.views import chatgpt_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('addpost/', views.add_post, name='addpost'),
    path('updatepost/<int:id>/', views.update_post, name='updatepost'),
    path('delete/<int:id>/', views.delete_post, name='deletepost'),
    path('api/', include('rest_api.urls')),
    path('books/', book_viewer, name='book_viewer'),
    path('chatgpt/', chatgpt_view, name='chatgpt'),
]

# probar con http://127.0.0.1:8000/miniblog/books/
