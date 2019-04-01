from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

import json
from .. import models
import pytz
from datetime import datetime
from django.conf import settings
from django.urls import reverse_lazy
from .mixin import MixinContext
from django.contrib.auth.mixins import UserPassesTestMixin
import requests
from ..serializers import CommentSerializer
from django.db import transaction

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

    def form_valid(self, form):
        try:
            with transaction.atomic():
                comment = form.save(commit=True)
                node = comment.post.get_node()
                if node:

                    # factory = APIRequestFactory()
                    # request = factory.get(settings.SITE_URL)
                    serializer_context = {
                        'request': Request(self.request),
                    }

                    r = requests.post(f"{node.endpoint}/posts/{comment.post.id}/comments", json={
                        "query": "addComment",
                        "post": comment.post.source,
                        "comment": CommentSerializer(comment, context=serializer_context).data
                    }, headers=node.getUserHeader(self.request.user.author))
                    print(r.text)
                    r.raise_for_status()

        except:
            pass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("post-id", kwargs={'pk': self.kwargs["post_pk"]})

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        if self.request.user.author.is_local_unverified_user():
            return False

        return True