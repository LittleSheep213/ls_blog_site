from django.contrib import admin
from .models import BlogType, Blog

# Register your models here.
@admin.register(BlogType)
class BlogTypeAdimn(admin.ModelAdmin):
	list_display = ("id", "type_name")

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "blog_type", "author", "read_num", "created_time", "last_updated_time")
# read_num 是Blog中的函数/方法

'''
@admin.register(ReadNum)
class ReadNumAdimn(admin.ModelAdmin):
	list_display = ("read_num", "blog")	
'''