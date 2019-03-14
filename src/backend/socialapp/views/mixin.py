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
                context['Posts'] = self.logged_user(Auth[0])
        else:
            context['Posts'] = self.public_user()

        return context



class DenyAcess(object):
	def deny(self):
		pass