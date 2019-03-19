from django.contrib import admin
from .models import ReadNum, ReadDetail

# Register your models here.
@admin.register(ReadNum)
class ReadNumAdimn(admin.ModelAdmin):
	list_display = ("read_num", "content_object")	


@admin.register(ReadDetail)
class ReadDetailAdimn(admin.ModelAdmin):
	list_display = ("read_num", "content_object", "date")	