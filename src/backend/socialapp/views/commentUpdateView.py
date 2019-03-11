from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site


import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy

class CommentUpdateView(UpdateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/comment-update.html'

    model = models.Comment
    fields = '__all__'
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:

            Auth = models.Author.objects.filter(localuser=self.request.user)
            if Auth:
                context['ActiveUser'] = Auth[0]
        return context

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        form_defaults = {
            "published": str(datetime.now())
        }
        return form_defaults