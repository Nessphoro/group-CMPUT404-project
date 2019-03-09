from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Author

class AuthorCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Author
        fields = ('username', 'email')

class AuthorChangeForm(UserChangeForm):

    class Meta:
        model = Author
        fields = ('username', 'email')