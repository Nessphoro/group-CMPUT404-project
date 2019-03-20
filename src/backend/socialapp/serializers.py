""" Serializers are used by the django-restframework library to configure the pages for individual objects.
    Register new models here.
"""
from .models import Author, Comment, Post, PostTags
from django.contrib.auth.models import User
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="author-id")

    class Meta:
        model = Author
        fields = ['id','url', 'host', 'displayName', 'github']
        # TODO, add URL field to Authors Serializer


class AuthorAltSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="author-id")
    friends = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id','url', 'host', 'displayName', 'github']
        # TODO, add URL field to Authors Serializer




class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)
    class Meta:
        model = Comment
        ordering = ["-published"]
        fields = ['author', 'comment', 'contentType', 'published', 'id']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        ordering = ["-published"]
        fields = ['title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories','comments', 'published', 'id', 'visibility', 'visibleTo', 'unlisted']