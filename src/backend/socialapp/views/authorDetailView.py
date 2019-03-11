from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json
from .. import models
import pytz
from datetime import datetime
from django.urls import reverse_lazy

#this should be update view
class AuthorDetailView(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/author-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get author image
        if self.request.user.is_authenticated:

            Auth = models.Author.objects.filter(localuser=self.request.user)
            if Auth:
                context['ActiveUser'] = Auth[0]
        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs) #probably not needed
        user = request.POST.get('displayName')
        descr = request.POST.get('bio')
        if user and descr:
            models.Author.objects.filter(localuser=self.request.user).update(displayName=user,bio=descr)
        return redirect('/Author')