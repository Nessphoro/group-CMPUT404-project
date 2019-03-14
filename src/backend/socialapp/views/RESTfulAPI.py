from django.contrib.auth.models import User
from rest_framework import viewsets
from .. import serializers
from .. import models
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """ Defines the pagination for a modelViewSet
    """
    page_size = 20
    page_size_query_param = 'size'
    max_page_size = 10000000



class AuthorViewSet(viewsets.ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    pagination_class = StandardResultsSetPagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    pagination_class = StandardResultsSetPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination


class PostTagsViewSet(viewsets.ModelViewSet):
    queryset = models.PostTags.objects.all()
    serializer_class = serializers.PostTagSerializer
    pagination_class = StandardResultsSetPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = StandardResultsSetPagination
