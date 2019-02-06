from author import Author
from django.db import models


class PostTags(models.Model):
    tag = models.CharField(max_length=64)
    
class Post(models.Model):
    title = models.CharField(max_length=150)
    source = models.URLField()
    origin = models.URLField()
    description = models.CharField(max_length = 280)
    contentType = models.CharField(max_length=64)
    content = models.TextField()
    author = models.ManyToOne(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(PostTags)
    published = models.DateTimeField()
    visibility = models.CharField(max_length=64)
    visibleTo = models.ManyToManyField(Author)
    unlisted = models.BooleanField()