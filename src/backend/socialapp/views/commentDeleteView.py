from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy
from .mixin import MixinContext


class CommentDeleteView(MixinContext,DeleteView):
    model = models.Comment
    success_url = reverse_lazy('index')

    # Get normally displays a deletion confirmation
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)