from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from collections import OrderedDict

from .. import serializers
from .. import models
from rest_framework.pagination import PageNumberPagination

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


class PublicPostsViewSet(ListAPIView):
    """
    Returns all the publicly visible posts in the format:
    {
        "query": "posts",
        "count": 1023,
        "size": 50,
        "next": "http://service/author/posts?page=5",
        "previous": "http://service/author/posts?page=3",
        "posts":[
            {
                "title":"A post title about a post about web dev",
                "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
                "origin":"http://whereitcamefrom.com/posts/zzzzz",
                "description":"This post discusses stuff -- brief",
                "contentType":"text/plain",
                "content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
                "author":{
                    "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "host":"http://127.0.0.1:5454/",
                    "displayName":"Lara Croft",
                    "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "github": "http://github.com/laracroft"
                },
                "categories":["web","tutorial"],
                "count": 1023,
                "size": 50,
                "next": "http://service/posts/{post_id}/comments",
                "comments":[
                    {
                        "author":{
                            "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                            "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                            "host":"http://127.0.0.1:5454/",
                            "displayName":"Greg Johnson",
                            "github": "http://github.com/gjohnson"
                        },
                        "comment":"Sick Olde English",
                        "contentType":"text/markdown",
                        "published":"2015-03-09T13:07:04+00:00",
                        "id":"de305d54-75b4-431b-adb2-eb6b9e546013"
                    }
                ]
                "published":"2015-03-09T13:07:04+00:00",
                "id":"de305d54-75b4-431b-adb2-eb6b9e546013",
                "visibility":"PUBLIC",
                "visibleTo":[],
                "unlisted":false
            }
        ]
    }
    """
    queryset = models.Post.objects.filter(visibility='PUBLIC',unlisted=False)
    serializer_class = serializers.PostSerializer
    pagination_class = PostsPagination

class PostViewSet(ListAPIView):
    # Returns a single post
    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # TODO: Check Author Has Permissions To See The Post
        # TODO: Check if Hindle actually wants this as a list of one item?
        post = get_object_or_404(models.Post, id= self.kwargs.get("pk"))
        return [post]

class PostCommentsViewSet(ListAPIView):
    # Returns a list of the comments attached to the post
    serializer_class = serializers.CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        post = get_object_or_404(models.Post, id=self.kwargs.get("pk"))

        return post.comments.all()

    # TODO: Bind this same url to take comments via POST and create them server side

class AuthorViewSet(ListAPIView):
    # Returns a single author
    serializer_class = serializers.AuthorAltSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # TODO: Check if Hindle actually wants this as a list of one item?
        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        return [author]




class AuthorFeedViewSet(ListAPIView):
    # Returns the logged in author's feed of posts
    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        author = self.request.user.author
        return author.get_all_posts()


class AuthoredByPostsViewSet(ListAPIView):
    # Returns all posts by a particular author denoted by author pk
    # Results may differ depending on authentication

    serializer_class = serializers.PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        author = get_object_or_404(models.Author, id= self.kwargs.get("pk"))
        return author.posts_by.all()


class FriendsViewSet(ListAPIView):
    pass

class isFriendsViewSet(ListAPIView):
    pass

class FriendsRequestViewSet(ListAPIView):
    pass
