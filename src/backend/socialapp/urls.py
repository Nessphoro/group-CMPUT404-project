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

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = ''

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('Author/', login_required(views.Author.as_view()), name='test1'),
    path('Comment/', views.Comment.as_view(), name='test2'),
    path('Post/', views.Post.as_view(), name='test3'),
    path('User/', views.User1.as_view(), name='test4'),
    path('api/',include(api_router.urls)),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--

]

#Alright, so, new plan, you have to change __init__.py to import all the classes, and change the url pattern to be more general. 