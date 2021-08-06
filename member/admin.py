from django.contrib import admin
# Register your models here.
from .models import *
from .models import Blog, Comment

class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname','email', 'password', 'created_at', 'updated_at')

admin.site.register(BoardMember, BoardMemberAdmin)
admin.site.register(Blog)
admin.site.register(Comment)