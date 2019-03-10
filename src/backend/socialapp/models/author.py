from django.contrib.auth.models import User
from django.db import models
import uuid
# from social_auth.signals import socialauth_registered

class Author(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    github = models.CharField(max_length=150, blank=False)
    displayName = models.CharField(max_length=150, blank=False)
    bio =  models.TextField(blank=True)
    host = models.URLField(blank=True)
    image = models.URLField(blank=True)
    feed = models.URLField(blank=True)
    localuser = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    friends = models.ManyToManyField("Author", blank=True, null=True, related_name="reverse_friends")

    def __str__(self):
        return "Author({},{},{})".format(self.displayName, self.localuser, self.github)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Author.objects.create(localuser=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


# def new_users_handler(sender, user, response, details, **kwargs):
#     user.is_new = True
#     f= open("log.txt","w+")
#     f.write(json.dumps(user))
#     f.write(json.dumps(response))
#     f.write(json.dumps(details))
#     f.close() 
#     return False

# socialauth_registered.connect(new_users_handler, sender=None)
