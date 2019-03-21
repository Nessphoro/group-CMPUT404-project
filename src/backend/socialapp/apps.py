from django.apps import AppConfig
from django.contrib.auth import get_user_model

class SocialappConfig(AppConfig):
    name = 'socialapp'

    def ready(self):
        User = get_user_model()
        try:
            User.objects.create_superuser('root', 'admin@admin.com', 'root')
        except:
            print("Root exists")
