from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .. import models
from .mixin import MixinContext

class AuthorDetailView(MixinContext,DetailView):
    template_engine = 'jinja2'
    template_name = 'socialapp/author-detail.html'
    model = models.Author

