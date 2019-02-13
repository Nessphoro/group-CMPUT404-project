from .author import Author
from django.db import models


class PostTags(models.Model):
    tag = models.CharField(max_length=64)
    
class Post(models.Model):
    id = models.UUIDField("id", primary_key=True)
    title = models.CharField(max_length=150)
    source = models.URLField()
    origin = models.URLField()
    description = models.CharField(max_length = 280)
    contentType = models.CharField(max_length=64)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author")
    categories = models.ForeignKey(PostTags, on_delete=models.CASCADE)
    published = models.DateTimeField()
    visibility = models.CharField(max_length=64)
    visibleTo = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="visibleTo")
    unlisted = models.BooleanField()