from .. import models
import aiohttp
import asyncio
from django.conf import settings
from django.urls import reverse_lazy
from urllib.parse import urlparse
import uuid
import base64
from django.contrib.auth.models import User


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
            if outstanding:
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



class MixinCreateAuthor(object):
    def createAuthor(self,data,requestType):
        if data["query"] ==requestType:
            author = data["author"]
            author_url = author["url"]
            path = urlparse(author_url).path
            author_id = None
            host = urlparse(author_url).netloc
            github = author["github"]
            displayName = author["displayName"]
            if path:
                author_id = path.split('/')[-1]
            # may need to readd this assumtion, or pull data from serve before checking this
            # remoteAuthor = models.Author(id=uuid.UUID(author_id),github=github,displayName=displayName,host=host)
            if models.Author.objects.filter(pk=author_id).exists():
                remoteAuthor = models.Author.objects.get(pk=author_id)
            for i in data["friends"]:
                host = urlparse(i).netloc
                author_id = None
                path = urlparse(i).path
                if path:
                    author_id = path.split('/')[-1]

                if models.Author.objects.filter(pk=author_id).exists():
                    fake_friend = models.Author.objects.get(pk=author_id)
                    remoteAuthor.friends.add(fake_friend)
            return remoteAuthor
        return None

class MixinCheckServer(object):
    def checkserver(self, server):
        if settings.LIMIT_NODE_TO_NODE_CONNECTIONS:
            server = server.split(' ')
            basic = server[0]
            auth = server[-1]
            decoded = base64.b64decode(auth).decode("utf-8").split('$')
            username = decoded[0]
            password = decoded[-1]

            print(username)
            print(password)
            if models.Node.objects.filter(endpoint=username).exists():
                node = models.Node.objects.get(endpoint=username)
                if node.password == password:
                    print('ye')
                    return True
                else:
                    print('no')
                    return False

            # if User.objects.filter(username=username).exists():
            #     user = User.objects.get(username=username)
            #     if user.check_password(password):
            #         return True
            #     else:
            #         return False
        else:
            return True