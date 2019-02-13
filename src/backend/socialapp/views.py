from django.shortcuts import render
from django.http import  HttpResponse
from rest_framework import viewsets
from . import serializers
from . import models
# Create your views here.


def index(req):
    return HttpResponse("Hello")

# API


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


