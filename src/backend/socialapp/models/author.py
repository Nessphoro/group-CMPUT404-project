from django.contrib.auth.models import User
# from django.contrib.sites.models import get_current_site
from .. import models as mod
from django.db import models
from django.urls import reverse
import uuid

class Author(models.Model):
    """ Authors represent a user in the social app's context, note they are distinct from users for modularity.

    Authors can establish relations to other authors on the site and to their github profile.

    Authors can make posts and comments which are the primary content of the site.
    """



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

    def get_friends(self):
        return set(self.friends)

    def get_friends_of_friends(self):
        output = set()

        for friend in self.friends.all():
            for friend_of_friend in friend.friends.all():
                output.add(friend_of_friend)

        return output

    def get_posts_of_friends(self):
        output = set()

        for f in self.friends.all():
            output = output | mod.Post.objects.filter(author=f,visibility='FRIENDS',unlisted=False)
        return output


    def get_posts_of_friends_of_friends(self):
        output = set()
        for f in self.friends.all():
            output = output | mod.Post.objects.filter(author=f,visibility='FOAF',unlisted=False)
            for fof in f.friends.all():
                output = output | mod.Post.objects.filter(author=f,visibility='FOAF',unlisted=False)
        return output

    def get_private(self):
        return set(mod.Post.objects.filter(visibleTo=self,unlisted=False))


    def is_friend(self, id):
        return friend.friends.filter(pk=id).exists() 

    def is_friend_of_friend(self, id):
        if self.friends.filter(pk=id).exists():
            return True
        else:
            #not calling fof because set is returned
            for friend in self.friends.all():
                if friend.friends.filter(pk=id).exists():
                    return True
        return False

    def get_my_feed(self):
        return set(mod.Post.objects.filter(author=self))

    def get_server(self): #todo
        # return set(models.Post.objects.filter(visibility='SERVERONLY',unlisted=False,origin=('http://'+get_current_site(request).domain)))
        return set()

    def get_public(self):
        return set(mod.Post.objects.filter(visibility='PUBLIC'))

    def post_permission(self, post):
        user = post.author
        visibility  = post.visibility

        if visibility=="PRIVATE":
            if user!=self:
                if post.visibleTo.filter(pk=self.id)==None:
                    return False 
        elif visibility=="FRIENDS" or visibility=="FOAF":
            if user.friends.filter(pk=self.id)==None:
                return False
            if visibility=="FOAF":
                for fof in user.friends.all():
                    if fof.friends.filter(pk=self.id)==None:
                        return False
        elif visibility=='SERVERONLY':
            # if ('http://'+get_current_site(request).domain) != post.origin:
            #     return False
            pass
        return True


    def get_all_posts(self):
        output = set()
        output |= self.get_my_feed()
        output |= self.get_posts_of_friends()
        output |= self.get_posts_of_friends_of_friends()
        output |= self.get_private()
        output |= self.get_server()
        output |= self.get_public()

        return output