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
    path('Author/<uuid:pk>', views.AuthorDetailView.as_view(), name='author-id'),

    path('Author/remove-friend/<uuid:target_pk>', views.AuthorActionsView.as_view(), {'action': 'remove-friend'},name='author-remove-friend'),

    path('Author/send-request/<uuid:target_pk>', views.AuthorActionsView.as_view(), {'action': 'send-friend-request'}, name='author-send-friend-request'),
    path('Author/accept-request/<uuid:target_pk>', views.AuthorActionsView.as_view(), {'action': 'accept-friend-request'}, name='author-accept-friend-request'),
    path('Author/decline-request/<uuid:target_pk>', views.AuthorActionsView.as_view(), {'action': 'decline-friend-request'}, name='author-decline-friend-request'),

    # Posts
    path('Post/<uuid:pk>/', views.PostDetailView.as_view(), name='post-id'),
    path('Post/<uuid:pk>/edit', views.PostUpdateView.as_view(), name='post-update'),
    path('Post/<uuid:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('Post/create/', views.PostCreateView.as_view(), name='post-create'),

    # Comments
    path('Comment/<uuid:post_pk>/create', views.CommentCreateView.as_view(), name='comment-create'),
    path('Comment/<uuid:pk>/edit', views.CommentUpdateView.as_view(), name='comment-update'),
    path('Comment/<uuid:pk>/delete', views.CommentDeleteView.as_view(), name='comment-delete'),

    # API - Should be done via the router
    path('api/',include(api_router.urls)),

    # Oauth - For Github Login, done by separate app
    url(r'^oauth/', include('social_django.urls' , namespace='social')),  # <--

    # Users
    path('logout', views.UserLogoutView.as_view(), name='logout')

]










#Alright, so, new plan, you have to change __init__.py to import all the classes, and change the url pattern to be more general.