from .author import Author
from .post import Post
from django.db import models
from django.urls import reverse
import uuid


class Comment(models.Model):
    """ Comments represent responses to a post by the authors who can view the post.

        TODO: Check if comments need to be in markdown as well.
    """



    # Django Metadata on class
    class Meta:
        ordering = ['-published'] # Order By Date Published By Default

    # Choices for certain fields
    CONTENT_TYPE_OPTIONS = {
        ('MARKDOWN','Markdown'),
        ('JPEG-IMAGE','Image (jpeg)'),
    }

    # Identifiers
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    # Relations
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="comments_by")
    post   = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    # Data
    comment = models.TextField()
    contentType = models.CharField(max_length=64, choices=CONTENT_TYPE_OPTIONS, default='MARKDOWN')
    published = models.DateTimeField()

    # Methods
    def __str__(self):
        return str(self.comment[:25])

    def get_edit_url(self):
        return reverse('comment-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('comment-delete', args=[str(self.id)])