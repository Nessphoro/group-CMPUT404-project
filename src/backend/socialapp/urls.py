from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers
from . import views

api_router = routers.DefaultRouter()
api_router.register(r'Author', views.AuthorViewSet)
api_router.register(r'Comment', views.CommentViewSet)
api_router.register(r'Post', views.PostViewSet)
api_router.register(r'PostTags', views.PostTagsViewSet)
api_router.register(r'User', views.UserViewSet)



urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('Author/', views.Author.as_view(), name='test1'),
    path('Comment/', views.Comment.as_view(), name='test2'),
    path('Post/', views.Post.as_view(), name='test3'),
    #path('User/', views.User.as_view(), name='test4'),
    path('api/',include(api_router.urls))
]

#Alright, so, new plan, you have to change __init__.py to import all the classes, and change the url pattern to be more general. 