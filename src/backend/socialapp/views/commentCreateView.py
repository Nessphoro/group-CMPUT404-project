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

class CommentCreateView(MixinContext,CreateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/comment-create.html'

    model = models.Comment
    fields = '__all__'
    success_url = reverse_lazy("index")

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        form_defaults = {
            "published": str(datetime.now())
        }

        if self.request.user.is_authenticated:
            form_defaults["author"] = self.request.user.author
            form_defaults["post"] = self.kwargs["post_pk"]

        return form_defaults