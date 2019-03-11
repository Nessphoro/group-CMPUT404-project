import json
from .models import Author
# import models
from django.contrib.auth.models import User
from django.db import models
import uuid

def save_profile(backend, user, response, *args, **kwargs):
    print(backend)
    if backend.name == 'github':
        if not Author.objects.filter(localuser=user):
            Author.objects.create(github=response['url'],localuser=user ,displayName=response['name'] ,image=response['avatar_url'] , feed=response['received_events_url'])