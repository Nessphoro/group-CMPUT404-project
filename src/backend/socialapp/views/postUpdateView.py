from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy
from .mixin import MixinContext
from .postCreateView import PostForm

class PostUpdateView(UserPassesTestMixin, MixinContext, UpdateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/post-update.html'
    model = models.Post
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super(PostUpdateView, self).get_form_kwargs()
        kwargs["author"] = self.request.user.author
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        # Paranoid
        self.object.author = self.request.user.author
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("post-id", kwargs={'pk': self.object.id})

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return self.get_object().author == self.request.user.author