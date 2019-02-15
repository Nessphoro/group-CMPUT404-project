from django.shortcuts import render
from django.http import  HttpResponse
from django.views.generic import TemplateView
from rest_framework import viewsets
from .. import serializers
from .. import models
# Create your views here.


class Index(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/socialapp_base.html'

    def get_context_data(self, **kwargs):
        pass


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


