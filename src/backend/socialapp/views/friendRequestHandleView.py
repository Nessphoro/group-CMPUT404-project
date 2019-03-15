from django.urls import reverse
from django.views.generic import RedirectView


from ..models import Author

class FriendRequestHandleView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        action = kwargs.get('action')

        if action == 'send_friend_request':
            author.send_friend_request(id)
            return reverse('')

        elif action == 'accept_friend_request':
            author.accept_friend_request(id)
            return reverse('')

        elif action == 'decline_friend_request':
            author.decline_friend_request(id)
            return reverse('')