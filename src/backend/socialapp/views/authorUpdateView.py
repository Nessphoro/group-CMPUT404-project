from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .. import models
from .mixin import MixinContext

class AuthorDetailView(MixinContext,UpdateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/author-update.html'
    model = models.Author

    fields = ["bio", "displayName"]

    def get_success_url(self):
        return self.get_object().get_absolute_url()