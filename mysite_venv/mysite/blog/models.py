from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_count.models import ReadNumExpandMethod, ReadDetail


class BlogType(models.Model): # 必须在Blog的上面
	type_name = models.CharField(max_length=15)

	def __str__(self):
		return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
	title = models.CharField(max_length=30)
	content = RichTextUploadingField()
	blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
	author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	read_details = GenericRelation(ReadDetail)
	created_time = models.DateTimeField(auto_now_add=True)
	last_updated_time = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return "<Blog:%s>"%self.title

	class Meta:  # 分页排序，一般最新的放在最前面，所以created_time前面有-号
		ordering = ['-created_time']


		
'''	def read_num(self):
		try:
			return self.readnum.read_num
		except exceptions.ObjectDoesNotExist as ReadNumNotExist:
			return 0
'''		

'''
class ReadNum(models.Model):	
	read_num = models.IntegerField(default=0)
	blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)
'''