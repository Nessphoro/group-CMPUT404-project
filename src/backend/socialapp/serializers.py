""" Serializers are used by the django-restframework library to configure the pages for individual objects.
    Register new models here.
"""
from .models import Author, Comment, Post, PostTags
from django.contrib.auth.models import User
from rest_framework import serializers


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostTags
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_superuser')