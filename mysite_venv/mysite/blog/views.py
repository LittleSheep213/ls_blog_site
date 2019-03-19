from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from read_count.utils import read_count_once
from .models import Blog, BlogType
from comment.models import Comment
from comment.forms import CommentForm


# Create your views here.
def get_blogs_data_needed(request, blogs_all_list):
	paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOG_NUM) # 每5篇进行分页
	page_num = request.GET.get('page', 1) # 获取url页码参数（GET请求）
	page_of_blogs = paginator.get_page(page_num) 
	current_page_num = page_of_blogs.number # 获取当前页码
	page_range = [x for x in range(int(page_num)-2, int(page_num)+3) if x>0 and x<=paginator.num_pages]

	# 添加省略页码标记
	if page_range[0] - 1 >= 2:
		page_range.insert(0, "…")
	if paginator.num_pages - page_range[-1] >= 2:
		page_range.append("…")
	# 首页和尾页
	if page_range[0] != 1:
		page_range.insert(0, 1)
	if page_range[-1] != paginator.num_pages:
		page_range.append(paginator.num_pages)

	# 获取不同日期归档的博客数
	blognum_of_date_list = {}
	for blog_date in Blog.objects.dates('created_time', 'month', order='ASC'):
		blog_count = Blog.objects.filter(created_time__year=blog_date.year, 
										 created_time__month=blog_date.month).count()
		blognum_of_date_list[blog_date] = blog_count

	content = {}
	content['page_of_blogs'] = page_of_blogs
	content["blog_types"] = BlogType.objects.all()
	content["page_range"] = page_range
	content["blog_dates"] = Blog.objects.dates('created_time', 'month', order='ASC')
	content["blognum_of_date_list"] = blognum_of_date_list
	return content


def blog_list(request):
	blogs_all_list = Blog.objects.all()
	content = get_blogs_data_needed(request, blogs_all_list)
	return render(request, "blog/blog_list.html", content)


def blogs_with_type(request, blog_type_pk):
	blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
	blogs_all_list = Blog.objects.filter(blog_type=blog_type)
	content = get_blogs_data_needed(request, blogs_all_list)
	content['blog_type'] = blog_type 	
	return render(request, "blog/blogs_with_type.html", content)


def blogs_with_date(request, year, month):
	blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
	content = get_blogs_data_needed(request, blogs_all_list)
	content['blogs_with_date'] = '%s年%s月' %(year, month) 
	return render(request, "blog/blogs_with_date.html", content)


def blog_detail(request, blog_pk):
	blog = get_object_or_404(Blog, pk = blog_pk)
	read_cookie_key = read_count_once(request, blog)
	blog_content_type = ContentType.objects.get_for_model(blog)
	comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)

	content = {}
	content["previous_blog"] = Blog.objects.filter(created_time__gt=blog.created_time).last()
	content["next_blog"] = Blog.objects.filter(created_time__lt=blog.created_time).first()
	content["blog"] = blog
	content["user"] = request.user
	content['comments'] = comments

	content['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model, 'object_id':blog_pk})

	response = render(request, "blog/blog_detail.html", content) # 响应
	response.set_cookie(read_cookie_key, 'true')  # 阅读标记
	return response