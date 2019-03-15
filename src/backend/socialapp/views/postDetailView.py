from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy
from .mixin import MixinContext
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



# @method_decorator(user_passes_test, name='dispatch')
class PostDetailView(MixinContext,UserPassesTestMixin,DetailView):
    template_engine = 'jinja2'
    template_name = 'socialapp/post-detail.html'
    model = models.Post

    def test_func(self):
        active = None
        post = self.get_object()
        user = post.author
        visibility  = post.visibility
        if self.request.user.is_authenticated:
            Auth = self.request.user.author
            return Auth.post_permission(post)
        if visibility != 'PUBLIC':
            return False
        # if active:
        #     if visibility=="PRIVATE":
        #         if user!=active:
        #             if post.visibleTo.filter(pk=active.id)==None:
        #                 return False 
        #     # elif visibility=="PRIVATE Author":
        #     #     if post.visibleTo!= active:
        #     #         return False
        #     elif visibility=="FRIENDS" or visibility=="FRIENDS OF FRIENDS":
        #         if user.friends.filter(pk=active.id)==None:
        #             return False
        #         if visibility=="FRIENDS OF FRIENDS":
        #             for fof in user.friends.all():
        #                 if fof.friends.filter(pk=active.id)==None:
        #                     return False
        # else:
        #     if visibility != 'PUBLIC':
        #         return False
        return True

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     if 'ActiveUser' in context:
    #         post = context['post']
    #         user = context['post'].author
    #         active = context['ActiveUser']
    #         visibility  = post.visibility

    #     return context


    # VISIBILITY_OPTIONS = {
    #     ('PUBLIC', 'Public'),
    #     ('PRIVATE', 'Private To Me'),
    #     ('PRIVATE Author', 'Private to Another Author'),
    #     ('FRIENDS', 'Private to Friends'),
    #     ('FRIENDS OF FRIENDS', 'Private to Friends of Friends'),
    # }
	#visibility