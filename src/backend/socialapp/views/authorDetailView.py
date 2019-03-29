from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import Http404
from .. import models
from .mixin import MixinContext
import aiohttp
import asyncio

class AuthorDetailView(MixinContext,DetailView):
    template_engine = 'jinja2'
    template_name = 'socialapp/author-detail.html'
    model = models.Author


    async def refresh_async(self, user, author: models.Author, node: models.Node):
        async with aiohttp.ClientSession() as session:
            outstanding = []
            outstanding.append(node.refreshRemoteAuthor(author, session))
            outstanding.append(node.refreshRemoteAuthorPosts(user, author, session))
            await asyncio.wait(outstanding)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(pk=pk)

        try:
            # Get the single item from the filtered queryset
            author = queryset.get()
            node = author.get_node()
            user = self.request.user.author if self.request.user.is_authenticated else None
            if node:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.refresh_async(user, author, node))
                author.refresh_from_db()
                loop.close()

            return author
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})

