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
from urllib.parse import urlparse

import json
import base64

from .mixin import MixinCreateAuthor, MixinCheckServer

# https://stackoverflow.com/questions/9626535/get-protocol-host-name-from-url
class StandardResultsSetPagination(PageNumberPagination):
    """ Defines the pagination for a modelViewSet
    """
    page_size = 20
    page_size_query_param = 'size'
    max_page_size = 100

class PostsPagination(PageNumberPagination):
    """ The spec wants to be clever with fields. Fine.
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

class PublicPostsViewSet(MixinCheckServer, ListAPIView):
    """ Returns a list of all public posts on the server, alternatively if the request came from a node this endpoint will return all posts on the server.
    """

    serializer_class = serializers.PostSerializer
    pagination_class = PostsPagination

    queryset = None
    def get_queryset(self):
        #todo check X-user
        server = self.request.META.get("HTTP_AUTHORIZATION") 
        user = self.request.META.get("HTTP_X-USER")
        if not server and not user:
            return models.Post.objects.filter(visibility='PUBLIC',unlisted=False)
        if self.checkserver(server):
            return models.Post.objects.all()
        else:
            return models.Post.objects.filter(visibility='PUBLIC',unlisted=False)



class PostViewSet(MixinCheckServer, MixinCreateAuthor, ListAPIView):
    """  Returns a single post in list form (as requested), per a post id specified in the url.
    """

    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        post = get_object_or_404(models.Post, id = self.kwargs.get("pk"))

        server = self.request.META.get("HTTP_AUTHORIZATION") 
        if server and self.checkserver(server):
            return [post]

        try:
            if post.visibility == 'PUBLIC':
                return [post]
            #todo  dont make this a cheap hack

            else:
                return [get_object_or_404(models.Post, id=None)] # HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')

        except:
            return [get_object_or_404(models.Post, id=None)] # HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')

    def post(self, request, *args, **kwargs):
        #todo need to change the error messages
        post = get_object_or_404(models.Post, id= self.kwargs.get("pk"))
        data = json.loads(request.body)
        try:
            remoteAuthor = self.createAuthor(data, "getPost")
        except Exception as e:
            return HttpResponseNotFound(f'<h1>look at this in the code to find the exception {e}</h1>')
        return self.has_pemission(data,post,remoteAuthor)

    def has_pemission(self,data, post,remoteAuthor):
        
        if remoteAuthor.post_permission(post):
            factory = APIRequestFactory()
            request = factory.get(data['url'])
            serializer_context = {
                'request': Request(request),
            }
            test = serializers.PostSerializer(post, context=serializer_context) #, context=request
            return JsonResponse(test.data)
        else:
            return HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')

        return HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')

class CommentsPagination(PageNumberPagination):
    """ The spec wants to be clever with fields. Fine.
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

class PostCommentsViewSet(MixinCreateAuthor, ListAPIView):
    """ Returns a list of the comments attached to the post as per the pk specified in the url.
    """

    serializer_class = serializers.CommentSerializer
    pagination_class = CommentsPagination

    # untested****
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        post = get_object_or_404(models.Post, id=pk)

        server = self.request.META.get("HTTP_AUTHORIZATION")
        if server and self.checkserver(server):
            return post.comments.all()

        try:
            if post.visibility == 'PUBLIC':
                return post.comments.all()
            #todo  dont make this a cheap hack
            else:

                return [get_object_or_404(models.Post, id=None)] # HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')
        except:
            return [get_object_or_404(models.Post, id=None)] # HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')

    def post(self, request, *args, **kwargs):
        #todo need to change the error messages

        post = get_object_or_404(models.Post, id= self.kwargs.get("pk"))
        comments = models.Comment.objects.all().filter(post=post)
        data = json.loads(request.body)

        try:
            remoteAuthor = self.createAuthor(data, "comments")
        except Exception as e:
            return HttpResponseNotFound(f'<h1>look at this in the code to find the exception {e}</h1>')

        return self.has_pemission(data, post,remoteAuthor, comments)

    def has_pemission(self,data, post,remoteAuthor, comments):

        if remoteAuthor.post_permission(post):

            factory = APIRequestFactory()
            request = factory.get(data['url'])
            serializer_context = {
                'request': Request(request),
            }
            page = self.paginate_queryset(comments)
            test = serializers.CommentSerializer(list(page), context=serializer_context,many=True)
            return JsonResponse(test.data, safe=False)
        else:
            return HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')
        return HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')

# TODO: Bind this same url to take comments via POST and create them server side

class AuthorViewSet(RetrieveAPIView):
    # Returns a single author
    serializer_class = serializers.AuthorAltSerializer
    queryset = models.Author.objects


#get with user credentials
class AuthorFeedViewSet(MixinCreateAuthor, ListAPIView):
    # Returns the logged in author's feed of posts
    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.META.get("HTTP_X_USER")
        url = self.check_author(user)

        author_id = None
        path = urlparse(url).path
        if path:
            author_id = path.split('/')[-1]

        if models.Author.objects.filter(pk=author_id).exists():
            author = models.Author.objects.get(pk=author_id)
        else:
            print("something went wrong")
        return author.get_my_feed()

    def check_author(self, user):
        url = decoded = base64.b64decode(user).decode("utf-8")
        return url

class AuthoredByPostsViewSet(MixinCreateAuthor, ListAPIView):
    # Returns all posts by a particular author denoted by author pk
    # Results may differ depending on authentication

    serializer_class = serializers.PostSerializer
    pagination_class = PostsPagination

    ##untested
    def get_queryset(self):
        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        server = self.request.META.get("HTTP_AUTHORIZATION") 
        if server and self.checkserver(server):
            return author.posts_by.all()

        # try:
        #     if post.visibility == 'PUBLIC':
        #         return author.posts_by.filter(visibility='PUBLIC')
        #     #todo  dont make this a cheap hack
        #     else:
        #         return [get_object_or_404(models.Post, id=None)] # HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')
        # except:
        #     return [get_object_or_404(models.Post, id=None)] # HttpResponseNotFound('<h1>Invalid u dont get this data</h1>')


    def get_queryset(self):

        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        return author.posts_by.all()

    def post(self, request, *args, **kwargs):
        #todo need to change the error messages

        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        data = json.loads(request.body)

        try:
            remoteAuthor = self.createAuthor(data, "posts")
        except Exception as e:
            return self.has_pemission(data, author,None)

        return self.has_pemission(data, author,remoteAuthor)

    def has_pemission(self,data, author,remoteAuthor):
        postSet = author.get_visitor(remoteAuthor)
        factory = APIRequestFactory()
        request = factory.get(data['url'])
        serializer_context = {
            'request': Request(request),
        }
        page = self.paginate_queryset(postSet)
        test = serializers.PostSerializer(list(page), context=serializer_context,many=True) 
        return JsonResponse(test.data, safe=False)

#this probably needs less credentials
class FriendsViewSet(MixinCheckServer, MixinCreateAuthor,ListAPIView):
    # Returns all friends of a particular author pk

    serializer_class = serializers.AuthorAltSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        test = self.request.META.get("HTTP_AUTHORIZATION") 
        if test and self.checkserver(test):
            friends = [ i.host+i.get_absolute_url() for i in author.friend_by.all()]
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
class isFriendsViewSet(ListAPIView):
    # Returns if author pk and another author are friends
    serializer_class = serializers.AuthorAltSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        author1 = get_object_or_404(models.Author, id= self.kwargs.get("pk1"))
        author2 = get_object_or_404(models.Author, id= self.kwargs.get("pk2"))
        are_friends = False
        if author1.is_friend(author2.id) and author2.is_friend(author1.id):
            are_friends = True

        data = {   "query":"friends",
                    "authors":[author1.host+author1.get_absolute_url(), author2.host+author2.get_absolute_url()],
                    "friends":are_friends,
                }
        return JsonResponse(data, safe=False)


class FriendsRequestViewSet(MixinCheckServer, MixinCreateAuthor, ListAPIView):
    # sends a friend request to user

    serializer_class = serializers.AuthorAltSerializer
    pagination_class = StandardResultsSetPagination

    # def get_queryset(self):

    #     author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
    #     return author.sent_friend_requests.all()

    # this is untested
    def post(self, request, *args, **kwargs):
        #todo need to change the error messages
        # author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        print("yeyey")
        data = json.loads(request.body)
        print(data['author'])
        try:
            author = self.createAuthor(data, "friendrequest")
        except Exception as e:
            print(e)
            return HttpResponseNotFound(f'<h1>look at this in the code to find the exception {e}</h1>')
        if 'author' in data:
            del data["author"]
        else:
            return HttpResponseNotFound("err")
        print('access')
        if 'friend':
            data['author'] = data.pop('friend')
        else:
            return HttpResponseNotFound("err")
        try:
            friend = self.createAuthor(data, "friendrequest")
        except Exception as e:
            return HttpResponseNotFound(f'<h1>look at this in the code to find the exception {e}</h1>')

        #todo request
        # print(author)
        try: 
            if author and friend:
                friend.friend_requests.add(author)
            else:

                return HttpResponseNotFound(f'<h1> none type error probABLY</h1>')
        except Exception as e:
            print(e)
            return HttpResponseNotFound(f'<h1>2: {e}</h1>')
        return HttpResponse('')

