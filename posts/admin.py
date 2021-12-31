from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, User, Class, Lesson, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(User, UserAdmin)
admin.site.register(Class)
admin.site.register(Lesson)
admin.site.register(Comment)