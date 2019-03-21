from .. import models
import aiohttp
import asyncio
from django.conf import settings
from django.urls import reverse_lazy

class MixinContext(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Auth = models.Author.objects.filter(localuser=self.request.user)
            # if Auth:
            context['ActiveUser'] = self.request.user.author
        return context


class MixinIndex(object):
    async def refresh_feed(self, session, active_user, url):
        async with session.get(url) as req:
            data = await req.json()
            for item in data:
                try:
                    itemId = int(item["id"])
                    if models.Post.objects.filter(correlationId=itemId):
                        continue
                    
                    title  = item['type']
                    description = "about Github"
                    content = "No Content"
                    timeAt = item["created_at"]

                    if title == "PushEvent":
                        description = f"I just pushed to my repository {item['repo']['name']}"
                    elif title == "ForkEvent":
                        description = f"I just forked {item['repo']['name']}"
                    elif title == "CreateEvent":
                        description = f"I just created {item['repo']['name']}"

                    title = "about Github"

                    post = models.Post(author=active_user, 
                                    origin=settings.SITE_URL, 
                                    source=settings.SITE_URL,
                                    title=title,
                                    description=description,
                                    content=content,
                                    contentType="text/markdown",
                                    published=timeAt,
                                    correlationId = itemId,
                                    unlisted=False
                                    )
                    post.save()

                    post.source = f"{settings.SITE_URL}{reverse_lazy('api-post', kwargs={'pk': post.id})}"
                    post.origin = post.source

                    post.save()
                    
                except Exception as e:
                    print(e)

    async def refresh_async(self, active_user):
        async with aiohttp.ClientSession() as session:
            
            outstanding = []
            if active_user:
                outstanding.append(self.refresh_feed(session, active_user, active_user.feed))
            for node in models.Node.objects.all():
                outstanding.append(node.pull(session))
            await asyncio.wait(outstanding)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get author image
        if self.request.user.is_authenticated:
            author = self.request.user.author
            context['ActiveUser'] = author
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.refresh_async(author))
            loop.close()
            context['Posts'] = author.get_all_posts()
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.refresh_async(None))
            loop.close()
            context['Posts'] = self.public_user()
        return context


# this is a build in mixin called UserPassesTestMixin and test_func
class DenyAcess(object):
	def deny(self):
		pass