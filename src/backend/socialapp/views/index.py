from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json
from .. import models


class Index(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get author image
        if self.request.user.is_authenticated:

            Auth = models.Author.objects.filter(localuser=self.request.user)
            if Auth:
                context['Author'] = Auth[0]
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
        pass

class User1(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/User.html'

    def get_context_data(self, **kwargs):
        pass
