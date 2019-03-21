from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Node)
class NodeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

