from django.contrib import admin

from .models import Author, Category, Post, Comment, PostView


class AuthorAdmin(admin.ModelAdmin):
    fields = ['user', 'profile_picture']
    list_display = ['user', 'profile_picture']
    list_filter = ['user']


admin.site.register(Author)

admin.site.register(Category)


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('AUTHOR', {'fields': ['author']}),
        ('CATEGORY', {'fields': ['categories']}),
        ('DESCRIPTION', {'fields': ['title', 'overview', 'thumbnail', 'content', 'featured']}),
        ('LINKS TO OTHER POST', {'fields': ['previous_post', 'next_post']})
    ]
    list_display = ['title', 'overview', 'author', 'timestamp', 'was_published_recently']
    list_filter = ['categories']
    search_fields = ['title', 'overview', 'content']


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    fields = ['user', 'post', 'content']
    list_filter = ['timestamp', 'post']
    list_display = ['user', 'post', 'content', 'was_published_recently']
    search_fields = ['user', 'post', 'content']


admin.site.register(Comment, CommentAdmin)


class PostViewAdmin(admin.ModelAdmin):
    fields = ['user', 'post']
    list_display = ['user', 'post']
    list_filter = ['post']
    search_fields = ['post']


admin.site.register(PostView, PostViewAdmin)
