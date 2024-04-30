from django.shortcuts import render
from django.http import Http404
# Create your views here.
# Contrucciòn del Rest
from rest_framework.response import Response
# Visualizaciòn del API Rest
from rest_framework.decorators import api_view
# Seguridad (Eliminar o activar)
from django.views.decorators.csrf import csrf_exempt
# Formato Json
from rest_framework.parsers import JSONParser
from rest_framework import status

from blog.models import Post
from .serializers import PostSerializer
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def lista_post(request):
    if request.method == 'GET':
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def vista_post(request, id):  # tomar de models los post // ojo el id es autorellenado
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        raise Http404("Post no encontrado")

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
