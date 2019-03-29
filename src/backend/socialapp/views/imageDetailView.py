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
import aiohttp
import asyncio


# @method_decorator(user_passes_test, name='dispatch')
class PostDetailView(MixinContext,UserPassesTestMixin,DetailView):
    template_engine = 'jinja2'
    template_name = 'socialapp/post-detail.html'
    model = models.Post

    async def refresh_async(self, author: models.Author, post: models.Post, node: models.Node):
        async with aiohttp.ClientSession() as session:
            outstanding = []
            outstanding.append(node.refreshRemotePost(author, post, session))
            outstanding.append(node.refreshRemoteComments(author, post, session))
            await asyncio.wait(outstanding)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        node = post.get_node()
        author = self.request.user.author if self.request.user.is_authenticated else None
        if node:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.refresh_async(author, post, node))
            loop.close()
        return context

    def test_func(self):
        #active = None
        post = self.get_object()
        visibility  = post.visibility
        if self.request.user.is_authenticated:
            Auth = self.request.user.author
            return Auth.post_permission(post)
        else:
            return False

        return True

