import datetime  # python自带的
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse
# from django.views.decorators.csrf import csrf_exempt
from read_count.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog
from .forms import LoginForm, RegForm



def get_week_hot_blogs():
	today = timezone.now().date()
	date = today - datetime.timedelta(days=7)
	blogs = Blog.objects.filter(read_details__date__lte=today, read_details__date__gt=date)\
						.values('id', 'title')\
						.annotate(read_num_sum=Sum('read_details__read_num'))\
						.order_by('-read_num_sum')
	return blogs[:7]


def home(request):
	blog_content_type = ContentType.objects.get_for_model(Blog)
	dates, read_nums = get_seven_days_read_data(blog_content_type)
	today_hot_data = get_today_hot_data(blog_content_type)
	yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
	# week_hot_blogs = get_week_hot_blogs()

	# 获取七天热门博客的缓存数据
	week_hot_blogs_cache = cache.get('week_hot_blogs_cache')
	if week_hot_blogs_cache is None:
		week_hot_blogs_cache = get_week_hot_blogs()
		cache.set('week_hot_blogs_cache', week_hot_blogs_cache, 60*60)

	content = {}
	content['dates'] = dates
	content['read_nums'] = read_nums
	content['today_hot_data'] = today_hot_data
	content['yesterday_hot_data'] = yesterday_hot_data
	content['week_hot_blogs'] = week_hot_blogs_cache
	return render(request, 'home.html', content)


# @csrf_exempt #增加装饰器，作用是跳过csrf中间件的保护，但这样做不安全
def Login(request):
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data['user']
			login(request, user)
			return redirect(request.GET.get('from', reverse('home')))
	else:
		login_form = LoginForm()
	content = {}
	content['login_form'] = login_form 
	return render(request, 'login.html', content)


def register(request):
	if request.method == 'POST':
		reg_form = RegForm(request.POST)
		if reg_form.is_valid():
			username = reg_form.cleaned_data['username']
			email = reg_form.cleaned_data['email']
			password = reg_form.cleaned_data['password_again']

			# 创建用户
			user = User.objects.create_user(username, email, password)
			user.save()
			# 登陆用户
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect(request.GET.get('from', reverse('home')))
			''' 也可以
			user = User()
			user.username = username
			user.email = email
			user.set_password = password
			user.save()
			'''
	else:
		reg_form = RegForm()

	content = {}
	content['reg_form'] = reg_form 
	return render(request, 'register.html', content)