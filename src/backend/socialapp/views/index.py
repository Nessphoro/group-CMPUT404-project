from django.views.generic import TemplateView

class Index(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/socialapp_base.html'

class Author(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Author.html'

class Comment(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Comment.html'

class Post(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/Post.html'

class User(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/User.html'

    def get_context_data(self, **kwargs):
        pass
