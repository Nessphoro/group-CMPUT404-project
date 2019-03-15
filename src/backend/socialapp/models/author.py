from django.contrib.auth.models import User
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
    followers = models.ManyToManyField("Author", blank=True, null=True, related_name="followed_by")
    friendrequests = models.ForeignKey("Author", blank=True, null=True, related_name="requested_by", on_delete=models.CASCADE)

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

    def send_friend_request(self):
        pass

    def accept_friend_request(self):
        pass

    def decline_friend_request(self):
        pass

    def check_foaf(self):
        pass

    def get_friends_of_friends(self):
        output = set()

        for friend in self.friends:
            for friend_of_friend in friend.friends:
                output.add(friend_of_friend)

        return output

    def get_posts_of_friends(self):
        pass


    def get_posts_of_friends_of_friends(self):
        pass









