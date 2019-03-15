from .. import models
class MixinContext(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Auth = models.Author.objects.filter(localuser=self.request.user)
            # if Auth:
            context['ActiveUser'] = self.request.user.author
        return context


class MixinIndex(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get author image
        if self.request.user.is_authenticated:
            author = self.request.user.author
            context['ActiveUser'] = author
            self.refresh_feed(author, author.feed)
            context['Posts'] = self.logged_user(author)
        else:
            context['Posts'] = self.public_user()

        return context


# this is a build in mixin called UserPassesTestMixin and test_func
class DenyAcess(object):
	def deny(self):
		pass