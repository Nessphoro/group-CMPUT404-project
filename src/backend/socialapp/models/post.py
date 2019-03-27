from .author import Author
from django.db import models
from django.urls import reverse
import uuid


class Post(models.Model):
    """ Posts represent a blog post in the application.

    Posts represent a user created entry, a post can be either an image post or a markdown post. Post content is
    to be base64 encoded.

    A posts's visibility may be limited to the author's friend group by one of the VISIBILITY_OPTIONS
    """

    # Django Metadata on class
    class Meta:
        ordering = ['-published'] # Order By Date Published By Default

    # Choices for certain fields
    VISIBILITY_OPTIONS = {
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private To Me (And Selected People)'),
        ('SERVERONLY', 'Public To This Host'),
        ('FRIENDS', 'Private to Friends'),
        ('FOAF', 'Private to Friends of Friends'),
    }

    CONTENT_TYPE_OPTIONS = {
        ('text/markdown','Markdown'),
        ('text/plain','Plain'),
        ('application/base64','File'),
        ('image/png;base64','PNG'),
        ('image/jpeg;base64','JPEG')
    }

    # Identifiers
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    correlationId = models.IntegerField(editable=False, default=-1, blank=True)

    # Relations
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts_by")
    visibleTo = models.ManyToManyField(Author, related_name="visibleTo", blank=True) #temporary

    # Data
    title = models.CharField(max_length=150)
    source = models.URLField()
    origin = models.URLField()
    description = models.CharField(max_length = 280)
    contentType = models.CharField(max_length=64, choices=CONTENT_TYPE_OPTIONS, default = "text/markdown")
    content = models.TextField()
    categories = models.CharField(max_length = 280, blank=True, default="")
    published = models.DateTimeField()
    visibility = models.CharField(max_length=64, choices=VISIBILITY_OPTIONS, default="PUBLIC") #temporary
    unlisted = models.BooleanField()

    # Methods
    def get_absolute_url(self):
        return reverse('post-id', args=[str(self.id)])

    def __str__(self):
        return str(self.title)


    def get_node(self):
        for node in mod.Node.objects.all():
            print(node.host)
            print(self.source)
            if node.host == self.source:
                return node