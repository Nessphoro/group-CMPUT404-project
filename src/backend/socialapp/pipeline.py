from .models import Author
from django.conf import settings


def save_profile(backend, user, response, *args, **kwargs):
    print(backend)
    if backend.name == 'github':
        if not Author.objects.filter(localuser=user):
            Author.objects.create(github=response['url'],localuser=user ,displayName=response['login'] ,image=response['avatar_url'] , feed=response['events_url'].replace("{/privacy}",""), host=settings.SITE_URL)


