from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import uuid

class Author(models.Model):

    # Django Metadata on class
    class Meta:
        ordering = ['displayName'] # Order By Display Name By Default

    # Identifiers
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    # Relations
    localuser = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    friends = models.ManyToManyField("Author", blank=True, null=True, related_name="friend_by")

    # Data
    github = models.CharField(max_length=150, blank=False)
    displayName = models.CharField(max_length=150, blank=False)
    bio =  models.TextField(blank=True)
    host = models.URLField(blank=True)
    image = models.URLField(blank=True)
    feed = models.URLField(blank=True)

    # Methods
    def __str__(self):
        return self.displayName

    def get_absolute_url(self):
        return reverse('author-id', args=[str(self.id)])