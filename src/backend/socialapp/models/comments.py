from .author import Author
from .post import Post
from django.db import models
import uuid


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.CharField(max_length=64)
    published = models.DateTimeField()

    def __str__(self):
        pass

