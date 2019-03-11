from .author import Author
from django.db import models
from django.urls import reverse
import uuid


class PostTags(models.Model):
    tag = models.CharField(max_length=64)


class Post(models.Model):

    # Django Metadata on class
    class Meta:
        ordering = ['-published'] # Order By Date Published By Default

    # Choices for certain fields
    VISIBILITY_OPTIONS = {
        ('PUBLIC', 'Public')
    }
    CONTENT_TYPE_OPTIONS = {
        ('MARKDOWN','Markdown'),
        ('JPEG-IMAGE','Image (jpeg)'),
    }

    # Identifiers
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    # Relations
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts_by")
    visibleTo = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="visibleTo", blank=True,null=True) #temporary

    # Data
    title = models.CharField(max_length=150)
    source = models.URLField()
    origin = models.URLField()
    description = models.CharField(max_length = 280)
    contentType = models.CharField(max_length=64, choices=CONTENT_TYPE_OPTIONS, default = "MARKDOWN")
    content = models.TextField()
    categories = models.ForeignKey(PostTags, on_delete=models.CASCADE, blank=True, null=True)
    published = models.DateTimeField()
    visibility = models.CharField(max_length=64, choices=VISIBILITY_OPTIONS, default="PUBLIC") #temporary
    unlisted = models.BooleanField()

    # Methods
    def get_absolute_url(self):
        return reverse('post-id', args=[str(self.id)])

    def __str__(self):
        return str(self.title)

