from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy
from .mixin import MixinContext

class PostUpdateView(MixinContext,UpdateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/post-update.html'

    model = models.Post
    fields = '__all__'
    success_url = reverse_lazy("index")
