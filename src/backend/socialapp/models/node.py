from django.db import models
from django.urls import reverse
import uuid
import aiohttp
from .author import Author
from .post import Post
from .comments import Comment
from django.conf import settings
import traceback
from urllib.parse import urlparse

class Node(models.Model):
    class Meta:
        ordering = ['friendlyName'] # Order By Display Name By Default

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    friendlyName = models.CharField(max_length=150, blank=False)
    endpoint = models.URLField(blank=False)
    password = models.CharField(max_length=150, blank=False)
    def __str__(self):
        return f"{self.endpoint}"
    
    @property
    def host(self):
        proto, host = urlparse(self.endpoint)[0:2]
        return f"{proto}://{host}"


    async def getOrCreateAuthor(session, author):
        authorId = author["id"].split("/")[-1]
        authors = Author.objects.filter(id=authorId)
        if authors:
            return authors[0]
        
        newAuthor = Author(
            id=authorId,
            host=author["host"],
            displayName=author["displayName"],
            github=author.get("github", "")
        )

        newAuthor.save()

        return newAuthor

    def getUserHeader(self, author):
        headers = {}
        if author:
            headers["X-User"] = f"{settings.SITE_URL}{reverse('api-author', kwargs={'pk': author.id})}"
        return headers
    
    def getUserEndpoint(self, author):
        if author:
            return f"{self.endpoint}/author/posts"
        else:
            return f"{self.endpoint}/posts"

    async def fetchRemoteAuthor(self, url, session: aiohttp.ClientSession):
        async with session.get(url) as r:
            data = await r.json()
            author = await Node.getOrCreateAuthor(session, data)
            author.firstName = data.get("firstName", "John")
            author.lastName = data.get("lastName", "Smith")
            author.email = data.get("email", "no@email.com")
            author.bio = data.get("bio", "No Bio")
            for a in data["friends"]:
                friend = Node.getOrCreateAuthor(a)
                if friend not in author.friends:
                    author.friends.add(friend)
                if author not in friend.friends:
                    friend.friends.add(author)
            author.save()
            return author

    async def refreshRemoteAuthor(self, author: Author, session: aiohttp.ClientSession):
        async with session.get(f"{self.endpoint}/author/{author.id}") as r:
            data = await r.json()
            # import pdb; pdb.set_trace()
            author.firstName = data.get("firstName", "John")
            author.lastName = data.get("lastName", "Smith")
            author.email = data.get("email", "no@email.com")
            author.bio = data.get("bio", "No Bio")
            for a in data["friends"]:
                friend = Node.getOrCreateAuthor(a)
                if friend not in author.friends:
                    author.friends.add(friend)
                if author not in friend.friends:
                    friend.friends.add(author)
            author.save()

    async def refreshRemoteAuthorPosts(self, author: Author, session: aiohttp.ClientSession):
        async with session.get(f"{self.endpoint}/author/{author.id}/posts") as r:
            data = await r.json()
            for post in data["posts"]:
                    if Post.objects.filter(id=post["id"]) or post['origin'].startswith(settings.SITE_URL):
                        continue
                    newPost = Post(author=author, 
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


    async def refreshRemotePost(self, post: Post, session: aiohttp.ClientSession):
        async with session.get(f"{self.endpoint}/posts/{post.id}") as r:
            data = await r.json()
            for post in data["posts"]:
                    if post['origin'].startswith(settings.SITE_URL):
                        return
                    if Post.objects.filter(id=post["id"]):
                        oldPost = Post.objects.filter(id=post["id"])[0]
                        oldPost.content = post["content"]
                        oldPost.title = post["title"]
                        oldPost.description = post["description"]
                        oldPost.save()
                        return
                    author = await Node.getOrCreateAuthor(session, post["author"])
                    newPost = Post(author=author, 
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

    async def refreshRemoteComments(self, post: Post, session: aiohttp.ClientSession):
        async with session.get(f"{self.endpoint}/posts/{post.id}/comments") as r:
            data = await r.json()
            for comment in data["comments"]:
                if Comment.objects.filter(id=comment["id"]):
                    continue
                
                author = await Node.getOrCreateAuthor(session, comment["author"])
                newComment = Comment(
                    id=comment["id"],
                    author=author,
                    post=post,
                    comment=comment["comment"],
                    contentType=comment["contentType"],
                    published=comment["published"]
                )
                newComment.save()

    async def pull(self, author, session: aiohttp.ClientSession):
        async with session.get(self.getUserEndpoint(author), headers=self.getUserHeader(author)) as response:
            try:
                data = await response.json()

                for post in data["posts"]:
                    if Post.objects.filter(id=post["id"]) or post['origin'].startswith(settings.SITE_URL):
                        continue
                    
                    postAuthor = await Node.getOrCreateAuthor(session, post["author"])
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
                traceback.print_exc()
                return