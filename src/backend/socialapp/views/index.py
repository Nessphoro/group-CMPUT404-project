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
from django.conf import settings


class Index(MixinIndex,TemplateView ):
    template_engine = 'jinja2'
    template_name = 'socialapp/index.html'

    #Todo, delete if not being used??
    def logged_user(self,active_user):
        # post = models.Post.objects
        self.refresh_feed(active_user, active_user.feed)
        post = models.Post.objects.filter(visibility='PUBLIC')
        for f in active_user.friends.all():
            if f.friends.filter(pk=active_user.id):   
                post = post | models.Post.objects.filter(author=f).filter(visibility='FRIENDS') # filter friend post
                post = post | models.Post.objects.filter(author=f).filter(visibility='FOAF') # filter friend post
            post = post | models.Post.objects.filter(author=f).filter(visibleTo=active_user)  # filter author post
            
            for fof in f.friends.all():
                if fof.friends.filter(pk=f.id): # bad
                    post = post | models.Post.objects.filter(author=fof).filter(visibility='FOAF') # filter friend post
        post = post.filter(unlisted=False)
        post = post | models.Post.objects.filter(author=active_user) #get all self posts
        active_user.get_posts_of_friends()
        return post

    def refresh_feed(self, active_user, url):
        req = requests.get(url)
        if req.status_code == 200:
            data = json.loads(req.content.decode('utf8'))
            for item in data:
                try:
                    itemId = int(item["id"])
                    if models.Post.objects.filter(correlationId=itemId):
                        continue
                    
                    title  = item['type']
                    description = "about Github"
                    content = "No Content"
                    timeAt = item["created_at"]

                    if title == "PushEvent":
                        description = f"I just pushed to my repository {item['repo']['name']}"
                    elif title == "ForkEvent":
                        description = f"I just forked {item['repo']['name']}"
                    elif title == "CreateEvent":
                        description = f"I just created {item['repo']['name']}"

                    title = "about Github"

                    p = models.Post(author=active_user, 
                                    origin=settings.SITE_URL, 
                                    source=settings.SITE_URL,
                                    title=title,
                                    description=description,
                                    content=content,
                                    contentType="text/markdown",
                                    published=timeAt,
                                    correlationId = itemId,
                                    unlisted=False
                                    )
                    p.save()
                except Exception as e:
                    print(e)
                    
        else:
            return None

    def public_user(self):
        return models.Post.objects.filter(visibility='PUBLIC',unlisted=False)

class Comment(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Comment.html'

    def get_context_data(self, **kwargs):
        pass
