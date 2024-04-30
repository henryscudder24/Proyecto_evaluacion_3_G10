from django.urls import path
from .views import lista_post, vista_post
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('post/', lista_post, name='lista_post'),
    # id de la BBDD
    path('post/<int:id>/', vista_post, name='vista_post'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]
