from .author import Author
from django.db import models
from django.urls import reverse
import uuid


class PostTags(models.Model):
    tag = models.CharField(max_length=64)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=150)
    source = models.URLField()
    origin = models.URLField()
    description = models.CharField(max_length = 280)
    contentType = models.CharField(max_length=64)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author")
    categories = models.ForeignKey(PostTags, on_delete=models.CASCADE, blank=True, null=True)
    published = models.DateTimeField()
    visibility = models.CharField(max_length=64, blank=True) #temporary
    visibleTo = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="visibleTo", blank=True,null=True) #temporary
    unlisted = models.BooleanField()

    def get_absolute_url(self):
        return reverse('post-id', args=[str(self.id)])

    def __str__(self):
        return str(self.id)

