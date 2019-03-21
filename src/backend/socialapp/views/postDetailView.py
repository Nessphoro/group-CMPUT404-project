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
        visibility  = post.visibility
        if self.request.user.is_authenticated:
            Auth = self.request.user.author
            return Auth.post_permission(post)
        if visibility != 'PUBLIC':
            return False

        return True

