from .models import Author
from django.conf import settings


def save_profile(backend, user, response, *args, **kwargs):
    # print(backend)
    # print(response)
    if backend.name == 'github':
        if not Author.objects.filter(localuser=user):
            firstName = response["name"].split()[0]
            lastName = response["name"].split()[1]
            Author.objects.create(github=response['html_url'], 
                                  email = response["email"],
                                  firstName = firstName,
                                  lastName = lastName,
                                  bio=response['bio'],
                                  localuser=user,
                                  displayName=response['login'],
                                  image=response['avatar_url'],
                                  feed=response['events_url'].replace("{/privacy}",""), 
                                  host=settings.SITE_URL)


