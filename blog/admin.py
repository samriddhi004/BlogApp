from django.contrib import admin
from .models import Author,Post,Tag,Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author","tag","date")
    list_display = ("title","excerpt","date","content")
    prepopulated_fields = {"slug":("title",)}
class CommentAdmin(admin.ModelAdmin):
    list_display=("user_name","post")
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment,CommentAdmin)