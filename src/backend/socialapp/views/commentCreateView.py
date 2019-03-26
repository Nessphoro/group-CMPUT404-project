from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site


import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy
from .mixin import MixinContext
from django.contrib.auth.mixins import UserPassesTestMixin

class CommentCreateView(UserPassesTestMixin, MixinContext,CreateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/comment-create.html'

    model = models.Comment
    fields = '__all__'

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        form_defaults = {
            "published": str(datetime.now())
        }

        if self.request.user.is_authenticated:
            form_defaults["author"] = self.request.user.author
            form_defaults["post"] = self.kwargs["post_pk"]

        return form_defaults

    def get_success_url(self):
        return reverse_lazy("post-id", kwargs={'pk': self.kwargs["post_pk"]})

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        if self.request.user.author.is_local_unverified_user():
            return False

        return True