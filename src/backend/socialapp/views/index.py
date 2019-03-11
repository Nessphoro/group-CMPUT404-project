from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json
from .. import models
import pytz
from datetime import datetime

class Index(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = models.Post.objects.all()
        context['Posts'] = post_list
        # get author image
        if self.request.user.is_authenticated:
            Auth = models.Author.objects.filter(localuser=self.request.user)
            # print(Auth)
            if Auth:
                context['Author'] = Auth[0]
            # else:
            #     context['Author'] = None 
        return context


class Author(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get author image
        if self.request.user.is_authenticated:

            Auth = models.Author.objects.filter(localuser=self.request.user)
            if Auth:
                context['Author'] = Auth[0]
        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs) #probably not needed
        user = request.POST.get('displayName')
        descr = request.POST.get('bio')
        if user and descr:
            models.Author.objects.filter(localuser=self.request.user).update(displayName=user,bio=descr)
        return redirect('/Author')

class Comment(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Comment.html'

    def get_context_data(self, **kwargs):
        pass

class Post(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] =  models.Post.objects.get(title=self.kwargs['title'])
        if self.request.user.is_authenticated:

            Auth = models.Author.objects.filter(localuser=self.request.user)
            if Auth:
                context['Author'] = Auth[0]
        return context

class NewPost(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/NewPost.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:

            Auth = models.Author.objects.filter(localuser=self.request.user)
            if Auth:
                context['Author'] = Auth[0]
        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs) #probably not needed
        Auth = models.Author.objects.filter(localuser=self.request.user)
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content')
        profile = None
        if title and description and content:
            profile = models.Post(title=title,source="http://127.0.0.1:8000/",origin="http://127.0.0.1:8000/",contentType='text',description=description,content=content,author=Auth[0], published=datetime.utcnow().replace(tzinfo=pytz.utc),unlisted=False)
            profile.save()
        if profile:
            return redirect(profile.get_absolute_url())
        return redirect('/')

class User1(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/User.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userAuthor'] =  models.Author.objects.get(github=self.kwargs['github'])

        if self.request.user.is_authenticated:

            Auth = models.Author.objects.filter(localuser=self.request.user)
            if Auth:
                context['Author'] = Auth[0]
        return context
