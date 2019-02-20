from django.contrib.auth.models import User
from django.db import models
import uuid

class Author(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    github = models.CharField(max_length=150, blank=False)
    displayName = models.CharField(max_length=150, blank=False)
    bio =  models.TextField()
    host = models.URLField()
    localuser = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    friends = models.ManyToManyField("Author", blank=True, null=True, related_name="reverse_friends")

    def __str__(self):
        return "Author({},{},{})".format(self.displayName, self.localuser, self.github)
