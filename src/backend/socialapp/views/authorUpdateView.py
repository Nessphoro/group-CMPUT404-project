from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from .. import models
from .mixin import MixinContext

class AuthorUpdateView(UserPassesTestMixin,MixinContext,UpdateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/author-update.html'
    model = models.Author

    fields = ["bio", "displayName"]

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return self.get_object() == self.request.user.author