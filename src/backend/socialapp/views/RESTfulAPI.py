from django.shortcuts import get_object_or_404
from django.http import JsonResponse,HttpResponseNotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView,ListCreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.http import HttpResponse
from collections import OrderedDict

from .. import serializers
from .. import models
from rest_framework.pagination import PageNumberPagination
from urllib.parse import urlparse, unquote

import json
import base64

import traceback
from .mixin import MixinCreateAuthor, MixinCheckServer

# https://stackoverflow.com/questions/9626535/get-protocol-host-name-from-url
class StandardResultsSetPagination(PageNumberPagination):
    """ 
    Defines the pagination for a modelViewSet.
    """
    page_size = 20
    page_size_query_param = 'size'
    max_page_size = 100

class PostsPagination(PageNumberPagination):
    """ 
    The spec wants to be clever with fields. Fine.
    """
    page_size = 100
    page_size_query_param = 'size'
    max_page_size = 200
    def get_paginated_response(self, data):
        """ Normalize fields
        """
        kvs = [
            ('query', 'posts'),
            ('count', self.page.paginator.count),
            ('size', self.page_size)
        ]

        if self.get_next_link():
            kvs.append(('next', self.get_next_link()))
        if self.get_previous_link():
            kvs.append(('previous', self.get_previous_link()))
        kvs.append(('posts', data))
            
        return Response(OrderedDict(kvs))

class PublicPostsViewSet(MixinCheckServer, MixinCreateAuthor, ListAPIView):
    """ Returns a list of all public posts on the server, alternatively if the request came from a node this endpoint will return all posts on the server.
    """

    serializer_class = serializers.PostSerializer
    pagination_class = PostsPagination

    queryset = None
    def get_queryset(self):
        #todo check X-user
        server = self.request.META.get("HTTP_AUTHORIZATION") 
        if self.checkserver(server):
            return models.Post.objects.filter(visibility='PUBLIC',unlisted=False)
        else:
            return []



class PostViewSet(MixinCheckServer, MixinCreateAuthor, ListAPIView):
    """  
    get:
    Returns a single post in list form (as requested), per a post id specified in the url.

    Please include the header for X-User in the form http:/service/author/id
    """

    serializer_class = serializers.PostSerializer
    pagination_class = PostsPagination

    def get_queryset(self):
        post = get_object_or_404(models.Post, id = self.kwargs.get("pk"))
        server = self.request.META.get("HTTP_AUTHORIZATION")
        if not self.checkserver(server):
            return []

        user = self.request.META.get("HTTP_X_USER")
        if user:
            author = self.createAuthor({"url": user}, "posts")
            print(f"X-User: {author}")
        else:
            author = None

        try:
            if post.visibility == 'PUBLIC':
                return [post]
            if not author:
                return []
            if author.post_permission(post):
                return [post]

        except:
            traceback.print_exc()
            return []
        return []

class CommentsPagination(PageNumberPagination):
    """ 
    The spec wants to be clever with fields. Fine.
    """
    page_size = 100
    page_size_query_param = 'size'
    max_page_size = 200
    def get_paginated_response(self, data):
        """ Normalize fields
        """
        kvs = [
            ('query', 'comments'),
            ('count', self.page.paginator.count),
            ('size', self.page_size)
        ]

        if self.get_next_link():
            kvs.append(('next', self.get_next_link()))
        if self.get_previous_link():
            kvs.append(('previous', self.get_previous_link()))
        kvs.append(('comments', data))
            
        return Response(OrderedDict(kvs))

class PostCommentsViewSet(MixinCreateAuthor, MixinCheckServer, ListAPIView):
    """ 
    get:
    Returns a list of the comments attached to the post as per the pk specified in the url.

    post:
    Adds a comment to a post if permissions allows it.
    """

    serializer_class = serializers.CommentSerializer
    pagination_class = CommentsPagination

    # untested****
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        post = get_object_or_404(models.Post, id=pk)

        server = self.request.META.get("HTTP_AUTHORIZATION")
        if not self.checkserver(server):
            return []

        user = self.request.META.get("HTTP_X_USER")
        if user:
            author = self.createAuthor({"url": user}, "posts")
            print(f"X-User: {author}")
        else:
            author = None

        try:
            if post.visibility == 'PUBLIC':
                return post.comments.all()
            if not author:
                return []
            if author.post_permission(post):
                return post.comments.all()
            else:
                return [] # HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')
        except:
            traceback.print_exc()
            return [] # HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')

    def post(self, request, *args, **kwargs):
        #todo need to change the error messages

        post = get_object_or_404(models.Post, id= self.kwargs.get("pk"))
        print(post)
        comments = models.Comment.objects.all().filter(post=post)
        data = json.loads(request.body)
        print(data)
        try:
            remoteAuthor = self.createAuthor(data["comment"]["author"], "addComments")
            if remoteAuthor.post_permission(post):
                c = models.Comment(
                    id=data["comment"]["id"],
                    author=remoteAuthor,
                    post = post,
                    comment=data["comment"]["comment"],
                    contentType=data["comment"]["contentType"],
                    published=data["comment"]["published"]
                )
                c.save()
                return JsonResponse({
                    "query": "addComment",
                    "success": True,
                    "message": "Comment Added"
                })
            else:
                return JsonResponse({
                    "query": "addComment",
                    "success": False,
                    "message": "Comment not allowed"
                })
        except Exception as e:
            print(e)
            traceback.print_exc()
            return HttpResponseNotFound(f'<h1>look at this in the code to find the exception {e}</h1>')

        return self.has_pemission(data, post,remoteAuthor, comments)

# TODO: Bind this same url to take comments via POST and create them server side

class AuthorViewSet(MixinCheckServer, RetrieveAPIView):
    """
    Returns a single author.
    """
    serializer_class = serializers.AuthorAltSerializer

    def get_queryset(self):
        server = self.request.META.get("HTTP_AUTHORIZATION")
        if not self.checkserver(server):
            return []
        return models.Author.objects
        

#get with user credentials
class AuthorFeedViewSet(MixinCreateAuthor, MixinCheckServer, ListAPIView):
    """
    Returns the logged in author's feed of posts.

    Please include the header for X-User in the form http:/service/author/id
    """
    serializer_class = serializers.PostSerializer
    pagination_class = PostsPagination

    def get_queryset(self):
        server = self.request.META.get("HTTP_AUTHORIZATION")
        if not self.checkserver(server):
            return []

        user = self.request.META.get("HTTP_X_USER")
        author = self.createAuthor({"url": user}, "posts")
        print(f"X-User: {author}")
        return author.get_all_posts()

    def check_author(self, user):
        return user

class AuthoredByPostsViewSet(MixinCreateAuthor, MixinCheckServer, ListAPIView):
    """
    Returns all posts by a particular author denoted by author pk.
    Results may differ depending on authentication.
    """

    serializer_class = serializers.PostSerializer
    pagination_class = PostsPagination

    ##untested
    def get_queryset(self):
        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        server = self.request.META.get("HTTP_AUTHORIZATION") 
        if not self.checkserver(server):
            return []

        user = self.request.META.get("HTTP_X_USER")
        visitor = self.createAuthor({"url": user}, "posts") if user else None
        print(f"X-User: {visitor}")

        return author.get_visitor(visitor)

#this probably needs less credentials
class FriendsViewSet(MixinCheckServer, MixinCreateAuthor,ListAPIView):
    """
    get:
    Returns all friends of a particular author pk.
    
    post:
    Asks if anyone in the list is friends with that author.
    """
    serializer_class = serializers.AuthorAltSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        test = self.request.META.get("HTTP_AUTHORIZATION") 
        if self.checkserver(test):
            friends = [ i.compute_full_id() for i in author.get_friends()]
            data = {   "query":"friends",
                        # 'author': author.id,
                        'authors': friends,
                    }
            return JsonResponse(data, safe=False)

        return JsonResponse({}, safe=False)

    # is this good enough? 
    def post(self, request, *args, **kwargs):
        #todo need to change the error messages
        print("access")
        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        data = json.loads(request.body)

        # friends = [ i.host+i.get_absolute_url() for i in author.friend_by.all()]
        friends = []
        if 'friends' in data:
            for i in data["friends"]:
                    host = urlparse(i).netloc
                    author_id = None
                    path = urlparse(i).path
                    if path:
                        author_id = path.split('/')[-1]
                        if author.is_friend(author_id):
                            friends.append(author_id)

        data = {   "query":"friends",
                    # 'author': author.id,
                    'authors': friends,
                }

        return JsonResponse(data, safe=False)


#should this be this class?
class isFriendsViewSet(MixinCheckServer, MixinCreateAuthor, ListAPIView):
    """
    Returns if author pk and another author are friends.
    """
    serializer_class = serializers.AuthorAltSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        server = self.request.META.get("HTTP_AUTHORIZATION") 
        if not self.checkserver(server):
            return []

        author1 = get_object_or_404(models.Author, id= self.kwargs.get("pk1"))
        author2 = self.createAuthor({"url": self.kwargs.get("pk2") }, "friendrequest")
        are_friends = False
        if author1.is_friend(author2.id) and author2.is_friend(author1.id):
            are_friends = True

        data = {   "query":"friends",
                    "authors":[author1.host+author1.get_absolute_url(), author2.host+author2.get_absolute_url()],
                    "friends":are_friends,
                }
        return JsonResponse(data, safe=False)


class FriendsRequestViewSet(MixinCheckServer, MixinCreateAuthor, ListAPIView):
    """
    Sends a friend request to user.
    """

    serializer_class = serializers.AuthorAltSerializer
    pagination_class = StandardResultsSetPagination

    def post(self, request, *args, **kwargs):
        server = self.request.META.get("HTTP_AUTHORIZATION") 
        if not self.checkserver(server):
            return []

        try: 
            print("yeyey")
            data = json.loads(request.body)
            print(data)
            author = self.createAuthor(data["author"], "friendrequest")
            friend = self.createAuthor(data["friend"], "friendrequest")
            if author and friend:
                if author in friend.friend_requests.all():
                    friend.accept_friend_request(author)
                else:
                    author.send_friend_request(friend)
            else:

                return HttpResponseNotFound(f'<h1> none type error probABLY</h1>')
        except Exception as e:
            print(e)
            traceback.print_exc()
            return HttpResponseNotFound(f'<h1>2: {e}</h1>')
        return HttpResponse('')

