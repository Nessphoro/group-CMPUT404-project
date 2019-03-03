from django.views.generic import TemplateView

class Index(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/socialapp_base.html'

    def get_context_data(self, **kwargs):
        pass

class Author(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Author.html'

    def get_context_data(self, **kwargs):
        pass

class Comment(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Comment.html'

    def get_context_data(self, **kwargs):
        pass

class Post(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Post.html'

    def get_context_data(self, **kwargs):
        pass

class User1(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/User.html'

    def get_context_data(self, **kwargs):
        pass
