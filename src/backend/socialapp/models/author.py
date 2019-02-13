from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    id = models.URLField("id", primary_key=True)
    github = models.CharField(max_length=150, blank=False)
    displayName = models.CharField(max_length=150, blank=False)
    bio =  models.TextField()
    host = models.URLField()
    localuser = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    friends = models.ForeignKey("Author", blank=True, on_delete=models.CASCADE, related_name="reverse_friends")