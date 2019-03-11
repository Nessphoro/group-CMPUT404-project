from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from django.conf.urls import url, include
from . import views

api_router = routers.DefaultRouter()
api_router.register(r'Author', views.AuthorViewSet)
api_router.register(r'Comment', views.CommentViewSet)
api_router.register(r'Post', views.PostViewSet)
api_router.register(r'PostTags', views.PostTagsViewSet)
api_router.register(r'User', views.UserViewSet)




urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    # Authors
    path('Author/', login_required(views.AuthorDetailView.as_view()), name='author'),
    path('User/<str:pk>/', views.User1.as_view(), name='test4'),

    # Posts
    path('Post/<uuid:pk>/', views.PostDetailView.as_view(), name='post-id'),
    path('Post/edit/<uuid:pk>', views.PostUpdateView.as_view(), name='post-update'),
    path('Post/delete/<uuid:pk>', views.PostDeleteView.as_view(), name='post-delete'),
    path('Post/create/', views.PostCreateView.as_view(), name='post-create'),

    # Comments
    path('Comment/', views.Comment.as_view(), name='test2'),
    path('Comment/create/', views.CommentCreateView.as_view(), name='comment-create'),

    # API - Should be done via the router
    path('api/',include(api_router.urls)),

    # Oauth - For Github Login, done by separate app
    url(r'^oauth/', include('social_django.urls' , namespace='social')),  # <--
]










#Alright, so, new plan, you have to change __init__.py to import all the classes, and change the url pattern to be more general.