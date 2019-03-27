""" Serializers are used by the django-restframework library to configure the pages for individual objects.
    Register new models here.
"""
from .models import Author, Comment, Post
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import fields
from django.urls import reverse
from django.conf import settings

class CategoryField(fields.ReadOnlyField):
    def __init__(self, **kwargs):
        super(CategoryField, self).__init__(**kwargs)

    def to_representation(self, value):
        if not value:
            return []
        return value.split(",")

class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name="api-author")
    url = serializers.HyperlinkedIdentityField(view_name="api-author")

    class Meta:
        model = Author
        fields = ['id', 'url', 'host', 'displayName', 'github']


class AuthorAltSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name="api-author")
    url = serializers.HyperlinkedIdentityField(view_name="api-author")
    friends = AuthorSerializer(many=True, read_only=True)
    # friend_requests = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'url', 'host', 'displayName', 'github', 'bio', 'friends']




class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)
   
    class Meta:
        model = Comment
        ordering = ["-published"]
        fields = ['author', 'comment', 'contentType', 'published', 'id']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    categories = CategoryField()
    # This is to deal with more indiosyncarcies of the spec
    count = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    next = serializers.SerializerMethodField()

    def get_count(self, obj):
        return len(obj.comments.all())
    
    def get_size(self, obj):
        return 20

    def get_next(self, obj):
        return f"{settings.SITE_URL}{reverse('api-post-comments', kwargs={'pk': obj.id})}"

    class Meta:
        model = Post
        ordering = ["-published"]
        fields = ['title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'size', 'next','comments', 'published', 'id', 'visibility', 'visibleTo', 'unlisted']