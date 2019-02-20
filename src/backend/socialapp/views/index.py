from django.views.generic import TemplateView

class Index(TemplateView):
    template_engine = 'jinja2'
    template_name = 'socialapp/socialapp_base.html'

    def get_context_data(self, **kwargs):
        pass
