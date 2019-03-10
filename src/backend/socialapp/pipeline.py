import json
from .models import Author
# import models
from django.contrib.auth.models import User
from django.db import models
import uuid

def save_profile(backend, user, response, *args, **kwargs):
    # f= open("log.txt","w+")
    # f.write(user)
    # f.write('\n')
    # f.write(json.dumps(backend.name))
    # f.write('\n')
    # f.write(json.dumps(response))
    # for i in args:
    #     f.write(i)
    #     f.write('\n')
    # for i in kwargs:
    #     f.write(i)
    #     f.write('\n')
    # f.close() 
    # pass
    if backend.name == 'github':
        profile = User.objects.get(username=user.username)
        if not profile:
            profile = Author(github=response['url'],localuser=user ,displayName=response['name'] ,image=response['avatar_url'] , feed=response['received_events_url'])
            profile.save()
