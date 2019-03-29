from django.views.generic import TemplateView, ListView, DetailView, CreateView
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        node = author.get_node()
        user = self.request.user.author if self.request.user.is_authenticated else None
        if node:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.refresh_async(user, author, node))
            loop.close()
        return context
