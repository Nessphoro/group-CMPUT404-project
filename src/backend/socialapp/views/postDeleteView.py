from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy


class PostDeleteView(DeleteView):
    model = models.Post
    success_url = reverse_lazy('index')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['post'] =  models.Post.objects.get(title=self.kwargs['title'])
        if self.request.user.is_authenticated:

            Auth = models.Author.objects.filter(localuser=self.request.user)
            if Auth:
                context['ActiveUser'] = Auth[0]
        return context


    # Get normally displays a deletion confirmation
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)