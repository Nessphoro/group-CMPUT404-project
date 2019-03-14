from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy
from .mixin import MixinContext

#this should be update view
class AuthorDetailView(MixinContext,DetailView):
    template_engine = 'jinja2'
    template_name = 'socialapp/author-detail.html'
    model = models.Author

