from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from .. import serializers
from .. import models
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """ Defines the pagination for a modelViewSet
    """
    page_size = 20
    page_size_query_param = 'size'
    max_page_size = 100





class PublicPostsViewSet(ListAPIView):
    # Returns all public posts on the server
    queryset = models.Post.objects.filter(visibility='PUBLIC',unlisted=False)
    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination


class AuthorFeedViewSet(ListAPIView):
    # TODO: Returns the authenticated author's feed of posts
    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        author = get_object_or_404(models.Author, id = self.request.query_params.get('pk'))
        return author.get_all_posts()


class AuthoredByPostsViewSet(ListAPIView):
    # Returns all posts by a particular author denoted by author pk
    # Results may differ depending on authentication

    serializer_class = serializers.PostSerializer
    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        return author.posts_by










"""
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
"""







