from django.db import models
from django.urls import reverse
import uuid
import aiohttp
from .author import Author
from .post import Post
from .comments import Comment
from django.conf import settings

class Node(models.Model):
    class Meta:
        ordering = ['friendlyName'] # Order By Display Name By Default

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    friendlyName = models.CharField(max_length=150, blank=False)
    endpoint = models.URLField(blank=False)

    def __str__(self):
        return f"{self.endpoint}"
    
    @property
    def host(self):
        return endpoint.partition("/")[0]


    async def getOrCreateAuthor(self, session, author):
        authorId = author["id"].split("/")[-1]
        authors = Author.objects.filter(id=authorId)
        if authors:
            return authors[0]
        
        newAuthor = Author(
            id=authorId,
            host=author["host"],
            displayName=author["displayName"],
            github=author["github"]
        )

        newAuthor.save()

        return newAuthor

    def getUserHeader(self, author):
        headers = {}
        if author:
            headers["X-User"] = f"{settings.SITE_URL}{reverse('api-author', kwargs={'pk': obj.id})}"
        return headers
    
    def getUserEndpoint(self, author):
        if author:
            return f"{self.endpoint}/author/posts"
        else:
            return f"{self.endpoint}/posts"

    async def pull(self, author, session: aiohttp.ClientSession):
        async with session.get(self.getUserEndpoint(author), headers=self.getUserHeader(author)) as response:
            try:
                data = await response.json()

                for post in data["posts"]:
                    if Post.objects.filter(id=post["id"]) or post['origin'].startswith(settings.SITE_URL):
                        continue
                    
                    postAuthor = await self.getOrCreateAuthor(session, post["author"])
                    newPost = Post( author=postAuthor, 
                                    origin=post["origin"], 
                                    source=f"{self.endpoint}/posts/{post['id']}",
                                    title=post["title"],
                                    description=post["description"],
                                    content=post["content"],
                                    contentType=post["contentType"],
                                    published=post["published"],
                                    unlisted=post["unlisted"],
                                    categories=",".join(post["categories"]),
                                    id=post["id"],
                                    visibility=post["visibility"]
                    )
                    newPost.save()
            except Exception as e:
                print(e)
                return