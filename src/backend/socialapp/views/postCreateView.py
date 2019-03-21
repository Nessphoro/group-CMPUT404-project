from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from django import forms

import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy
from .mixin import MixinContext
from django.conf import settings

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = '__all__'
    
    
    def __init__(self, *args, **kwargs):
        author = kwargs.pop("author")
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["visibleTo"].queryset = models.Author.objects.exclude(id=author.id)

class PostCreateView(MixinContext,CreateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/post-create.html'

    form_class = PostForm
    
    success_url = reverse_lazy("index")

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs["author"] = self.request.user.author
        return kwargs

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        form_defaults = {
            "source": settings.SITE_URL,
            "origin": settings.SITE_URL,
            "published": str(datetime.now()),
            "author": self.request.user.author
        }
        return form_defaults

    def get_success_url(self):
        return reverse_lazy("post-id", kwargs={'pk': self.object.id})

