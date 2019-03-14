""" This file defines the urls patterns used by socialapp.
    The api_router automatically controls the API related links.
"""

from django.urls import path
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from django.conf.urls import url, include
from . import views

api_router = routers.DefaultRouter()
api_router.register(r'author', views.AuthorViewSet)
api_router.register(r'posts', views.PostViewSet)
api_router.register(r'posttags', views.PostTagsViewSet)
api_router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    # Authors
    path('Author/<uuid:pk>', login_required(views.AuthorDetailView.as_view()), name='author-id'),
    # path('User/<str:pk>/', views.User1.as_view(), name='test4'), # TODO: I don't know if this is still used

    # Posts
    path('Post/<uuid:pk>/', views.PostDetailView.as_view(), name='post-id'),
    path('Post/edit/<uuid:pk>', views.PostUpdateView.as_view(), name='post-update'),
    path('Post/delete/<uuid:pk>', views.PostDeleteView.as_view(), name='post-delete'),
    path('Post/create/', views.PostCreateView.as_view(), name='post-create'),

    # Comments
    path('Comment/create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('Comment/edit/<uuid:pk>', views.CommentUpdateView.as_view(), name='comment-update'),
    path('Comment/delete/<uuid:pk>', views.CommentDeleteView.as_view(), name='comment-delete'),

    # API - Should be done via the router
    path('api/',include(api_router.urls)),

    # Oauth - For Github Login, done by separate app
    url(r'^oauth/', include('social_django.urls' , namespace='social')),  # <--
]










#Alright, so, new plan, you have to change __init__.py to import all the classes, and change the url pattern to be more general.