from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy
from .mixin import MixinContext


class CommentDeleteView(UserPassesTestMixin,MixinContext,DeleteView):
    model = models.Comment
    success_url = reverse_lazy('index')

    # Get normally displays a deletion confirmation
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("post-id", kwargs={'pk': self.get_object().post.id})

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return self.get_object().author == self.request.user.author