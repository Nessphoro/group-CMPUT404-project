from .. import models
class MixinContext(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            Auth = models.Author.objects.filter(localuser=self.request.user)
            if Auth:
                context['ActiveUser'] = Auth[0]
        return context


class MixinIndex(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get author image
        if self.request.user.is_authenticated:
            Auth = models.Author.objects.filter(localuser=self.request.user)
            if Auth:
                context['ActiveUser'] = Auth[0]
                context['Posts'] = Auth[0].get_all_posts()
                self.refresh_feed(Auth[0], Auth[0].feed)
        else:
            context['Posts'] = self.public_user()

        return context


# this is a build in mixin called UserPassesTestMixin and test_func
class DenyAcess(object):
	def deny(self):
		pass