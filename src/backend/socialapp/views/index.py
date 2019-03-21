from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy
from .mixin import MixinContext, MixinIndex


class Index(MixinIndex,TemplateView ):
    template_engine = 'jinja2'
    template_name = 'socialapp/index.html'

    def public_user(self):
        return models.Post.objects.filter(visibility='PUBLIC',unlisted=False)

class Comment(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Comment.html'

    def get_context_data(self, **kwargs):
        pass
