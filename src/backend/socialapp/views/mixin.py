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
                # import pdb; pdb.set_trace()
                outstanding.append(node.pull(active_user, session))
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
            context['Posts'] = author.get_all_posts()[:50]
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


async def fetchUser(url, node):
    async with aiohttp.ClientSession() as session:
        return await node.fetchRemoteAuthor(url, session, True)

async def refreshUser(author, node):
    async with aiohttp.ClientSession() as session:
        return await node.refreshRemoteAuthor(author, session, True)

class MixinCreateAuthor(object):
    def createAuthor(self,author,requestType):
        author_url = author["url"]
        path = urlparse(author_url).path
        author_id = None
        if path:
            author_id = path.split('/')[-1]
        # may need to readd this assumtion, or pull data from serve before checking this
        # remoteAuthor = models.Author(id=uuid.UUID(author_id),github=github,displayName=displayName,host=host)
        

        if models.Author.objects.filter(pk=author_id).exists():
            remoteAuthor = models.Author.objects.get(pk=author_id)
            node = generic_find_node(author_url)
            if node:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                remoteAuthor = loop.run_until_complete(refreshUser(remoteAuthor, node))
                loop.close()

        else:
            node = generic_find_node(author_url)
            if not node:
                raise Exception("Node not found")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            remoteAuthor = loop.run_until_complete(fetchUser(author_url, node))
            loop.close()
        return remoteAuthor

class MixinCheckServer(object):
    def checkserver(self, server):
        if settings.LIMIT_NODE_TO_NODE_CONNECTIONS:
            if not server:
                raise Exception("No Authorization Header")
            server = server.split(' ')
            basic = server[0]
            auth = server[-1]
            username, _, password = base64.b64decode(auth).decode("utf-8").rpartition(':')
            print(username)
            password = password.strip()
            print(f"{password}:{len(password)}")
            node = generic_find_node(username)


            if node:
                print("Found node")
                print(node)
                print(f"{node.password}:{len(node.password)}")
                if node.password == password:
                    return True
                else:
                    return False
            print("No Node")
            return False
            # if User.objects.filter(username=username).exists():
            #     user = User.objects.get(username=username)
            #     if user.check_password(password):
            #         return True
            #     else:
            #         return False
        else:
            return True


def generic_find_node(url) -> models.Node:
    proto, host = urlparse(url)[0:2]
    host = f"{proto}://{host}"
    for node in models.Node.objects.all():
            print(node.host)
            print(host)
            if node.host == host:
                return node