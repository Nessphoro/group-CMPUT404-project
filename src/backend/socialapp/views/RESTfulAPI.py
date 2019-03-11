from django.contrib.auth.models import User
from rest_framework import viewsets
from .. import serializers
from .. import models

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


class PostTagsViewSet(viewsets.ModelViewSet):
    queryset = models.PostTags.objects.all()
    serializer_class = serializers.PostTagSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


#class TestViewSet(viewsets.ModelViewSet):
    #queryset = 