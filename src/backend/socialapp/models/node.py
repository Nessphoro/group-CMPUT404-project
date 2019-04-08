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
    basicToken = models.CharField(max_length=300, blank=True, default="")

    def __str__(self):
        return f"{self.endpoint}"
    
    @property
    def host(self):
        proto, host = urlparse(self.endpoint)[0:2]
        return f"{proto}://{host}"


    async def getOrCreateAuthor(session, author, full=False):
        authorId = author["id"].split("/")[-1]
        authors = Author.objects.filter(id=authorId)
        if authors:
            newAuthor = authors[0]
        else:
            github = author.get("github", "")
            if not github:
                github = ""
            newAuthor = Author(
                id=authorId,
                host=author["host"],
                displayName=author["displayName"],
                github=github
            )

            newAuthor.save()
        
        if full:
            node = newAuthor.get_node()
            if node:
                newAuthor = await node.refreshRemoteAuthor(newAuthor, session, False)

        return newAuthor

    def getUserHeader(self, author):
        headers = {}
        if author:
            headers["X-User"] = f"{settings.SITE_URL}{reverse('api-author', kwargs={'pk': author.id})}"
        if self.basicToken:
            headers["Authorization"] = f"Basic {self.basicToken}"
        return headers
    
    def getUserEndpoint(self, author):
        if author:
            return f"{self.endpoint}/author/posts"
        else:
            return f"{self.endpoint}/posts"

    async def fetchRemoteAuthor(self, url, session: aiohttp.ClientSession, full=False):
        async with session.get(url, headers=self.getUserHeader(None)) as r:
            data = await r.json()
            author = await Node.getOrCreateAuthor(session, data)
            author.host = data.get("host", "invalid.host.com")
            author.firstName = data.get("firstName", "John")
            author.lastName = data.get("lastName", "Smith")
            author.email = data.get("email", "no@email.com")
            author.bio = data.get("bio", "No Bio")
            author.image = data.get("image", f"{settings.SITE_URL}/static/socialapp/question-mark-face.jpg")
            author.save()
            for a in data["friends"]:
                friend = await Node.getOrCreateAuthor(session, a, full)
                if friend not in author.friends.all():
                    author.friends.add(friend)
                if author not in friend.friends.all():
                    friend.friends.add(author)
            author.save()
            return author

    async def refreshRemoteAuthor(self, author: Author, session: aiohttp.ClientSession, full=False):
        async with session.get(f"{self.endpoint}/author/{author.id}", headers=self.getUserHeader(None)) as r:
            try:
                r.raise_for_status()
                data = await r.json()
                # import pdb; pdb.set_trace()
                author.firstName = data.get("firstName", "John")
                author.host = data.get("host", "invalid.host.com")
                author.lastName = data.get("lastName", "Smith")
                author.displayName = data.get("displayName", "User")
                author.email = data.get("email", "no@email.com")
                author.image = data.get("image", f"{settings.SITE_URL}/static/socialapp/question-mark-face.jpg")
                author.bio = data.get("bio", "No Bio")
                for a in data["friends"]:
                    friend = await Node.getOrCreateAuthor(session, a, full)
                    if friend not in author.friends.all():
                        author.friends.add(friend)
                    if author not in friend.friends.all():
                        friend.friends.add(author)
                author.save()
                return author
            except Exception as e:
                print(f"Error in {self.endpoint}")
                # print(await r.text())
                traceback.print_exc()
                return author

    async def refreshRemoteAuthorPosts(self, requestor: Author, author: Author, session: aiohttp.ClientSession):
        async with session.get(f"{self.endpoint}/author/{author.id}/posts", headers=self.getUserHeader(requestor)) as r:
            data = await r.json()
            for post in data["posts"]:
                    if Post.objects.filter(id=post["id"]):
                        if not post['origin'].startswith(settings.SITE_URL):
                            oldPost = Post.objects.filter(id=post["id"])[0]
                            oldPost.visibility = oldPost.visibility.upper() # Fix shitty servers not returning all upper cased visiblitiy
                            oldPost.save()
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


    async def refreshRemotePost(self, author: Author, post: Post, session: aiohttp.ClientSession):
        async with session.get(f"{self.endpoint}/posts/{post.id}", headers=self.getUserHeader(author)) as r:
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

    async def refreshRemoteComments(self, author: Author, post: Post, session: aiohttp.ClientSession):
        async with session.get(f"{self.endpoint}/posts/{post.id}/comments", headers=self.getUserHeader(author)) as r:
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
                    if Post.objects.filter(id=post["id"]):
                        if not post['origin'].startswith(settings.SITE_URL):
                            oldPost = Post.objects.filter(id=post["id"])[0]
                            oldPost.visibility = oldPost.visibility.upper() # Fix shitty servers not returning all upper cased visiblitiy
                            oldPost.save()
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
                print(f"Error in {self.endpoint}")
                print(await response.text())
                traceback.print_exc()
                return