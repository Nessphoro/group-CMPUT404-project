from author import Author
from post import Post
from django.db import models

class Comment(models.Model):
    id = models.UUIDField("id", primary_key=True)
    author = models.ManyToOne(Author, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.CharField(max_length=64)
    published = models.DateTimeField()