from django.urls import reverse_lazy
from django.shortcuts import  get_object_or_404
from django.views.generic import RedirectView


from ..models import Author



class AuthorActionsView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        action  = kwargs.get('action')
        target_pk = kwargs.get('target_pk')

        if action == "send-friend-request":
            self.send_friend_request(target_pk)

        if action == "remove-friend":
            self.remove_friend(target_pk)

        if action == "accept-friend-request":
            self.accept_friend_request(target_pk)

        if action == "decline-friend-request":
            self.decline_friend_request(target_pk)

        return reverse_lazy('index')


    def send_friend_request(self, target_pk):
        sender = self.request.user.author
        target = get_object_or_404(Author, id=target_pk)

        sender.send_friend_request(target)

    def remove_friend(self, target_pk):
        unfriender = self.request.user.author
        target = get_object_or_404(Author, id=target_pk)

        unfriender.remove_from_friends(target)

    def accept_friend_request(self, sender_pk):
        sender  = get_object_or_404(Author, id=sender_pk)
        target  = self.request.user.author

        target.accept_friend_request(sender)

    def decline_friend_request(self, sender_pk):
        sender  = get_object_or_404(Author, id=sender_pk)
        target  = self.request.user.author

        target.decline_friend_request(sender)




