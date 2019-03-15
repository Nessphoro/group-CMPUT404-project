from django.urls import reverse
from django.views.generic import RedirectView


from ..models import Author

class FriendRequestHandleView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        action = kwargs.get('action')
        id = kwargs.get('pk')

        author = self.request.user.author

        print(author)

        if action == 'send_friend_request':
            author.send_friend_request(id)
            return reverse('author-id', kwargs=[self.request.user.author.id])

        elif action == 'accept_friend_request':
            author.accept_friend_request(id)
            return reverse('author-id', kwargs=[self.request.user.author.id])

        elif action == 'decline_friend_request':
            author.decline_friend_request(id)
            return reverse('author-id', kwargs=[self.request.user.author.id])