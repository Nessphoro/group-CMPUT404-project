from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy
import requests
from .mixin import MixinContext, MixinIndex


class Index(MixinIndex,TemplateView ):
    template_engine = 'jinja2'
    template_name = 'socialapp/index.html'

    def logged_user(self,active_user):
        # post = models.Post.objects
        post = models.Post.objects.filter(visibility='PUBLIC')
        for f in active_user.friends.all():
            if f.friends.filter(pk=active_user.id):   
                post = post | models.Post.objects.filter(author=f).filter(visibility='FRIENDS') # filter friend post
                post = post | models.Post.objects.filter(author=f).filter(visibility='FRIENDS OF FRIENDS') # filter friend post
            post = post | models.Post.objects.filter(author=f).filter(visibleTo=active_user)  # filter author post
            
            for fof in f.friends.all():
                if fof.friends.filter(pk=f.id): # bad
                    post = post | models.Post.objects.filter(author=fof).filter(visibility='FRIENDS OF FRIENDS') # filter friend post
        post = post.filter(unlisted=False)
        post = post | models.Post.objects.filter(author=active_user) #get all self posts

        #warning, queryset is converted into a list after this, cant use filter
        feed = self.get_feed(active_user.feed)
        if feed: 
            post = self.feed_processing(feed,post,active_user)


        return post

    def get_feed(self,url):
        req = requests.get(url)
        if req.status_code ==200:
            return  json.loads(req.content.decode('utf8')) #in dictojary format
        else:
            return None

    def feed_processing(self,feed,post,active_user):
        post = list(post)
        for item in feed:
            try:
                title  = item['type'] #+ ": " + item['repo']['name']
                description = item['type']
                payload = item['repo']['url']
                date = item['created_at']
                name = item['repo']['name']
                add_feed = models.Post(author=active_user,title=title, source=payload,origin=payload,contentType='GITHUB',description=name,content=name,unlisted=False)
                post.append(add_feed)
            except KeyError: #this should be logged
                pass
        return post

    def public_user(self):
        return models.Post.objects.filter(visibility='PUBLIC')

class Comment(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Comment.html'

    def get_context_data(self, **kwargs):
        pass

class NewPost(MixinContext,CreateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/post-create.html'
    model = models.Post
    fields = '__all__'

    def get_success_url(self):
        # return redirect(self.model.get_absolute_url())
        return reverse_lazy('test3',kwargs={'pk':str(self.object.id)})

    # def post(self, request, *args, **kwargs):
    #     context = super().get_context_data(**kwargs) #probably not needed
    #     Auth = models.Author.objects.filter(localuser=self.request.user)
    #     title = request.POST.get('title')
    #     description = request.POST.get('description')
    #     content = request.POST.get('content')
    #     profile = None
    #     if title and description and content:
    #         profile = models.Post(title=title,source="http://127.0.0.1:8000/",origin="http://127.0.0.1:8000/",contentType='text',description=description,content=content,author=Auth[0], published=datetime.utcnow().replace(tzinfo=pytz.utc),unlisted=False)
    #         profile.save()
    #     if profile:
    #         return redirect(profile.get_absolute_url())
    #     return redirect('/')

# this needs to change, but i chose a bad context variable
# i think i may need to change context['Author'] to something else
class User1(MixinContext,DetailView):
    template_engine = 'jinja2'
    template_name = 'socialapp/User.html'
    model = models.Author

