from .models import Author
from django.conf import settings


def save_profile(backend, user, response, *args, **kwargs):
    # print(backend)
    # print(response)
    if backend.name == 'github':
        if not Author.objects.filter(localuser=user):
            try:
                firstName = response["name"].split()[0]
            except:
                firstName = "John"
            try:
                lastName = response["name"].split()[1]
            except:
                lastName = "Smith"
            bio = response['bio']
            if not bio:
                bio = "No bio"
            Author.objects.create(github=response['html_url'], 
                                  email = response["email"],
                                  firstName = firstName,
                                  lastName = lastName,
                                  bio=bio,
                                  localuser=user,
                                  displayName=response['login'],
                                  image=response['avatar_url'],
                                  feed=response['events_url'].replace("{/privacy}",""), 
                                  host=settings.SITE_URL)


