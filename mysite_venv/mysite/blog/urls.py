from django.urls import path
from .views import blog_detail, blogs_with_type, blog_list, blogs_with_date

urlpatterns = [
	path('', blog_list, name='blog_list'),
	# http://localhost:8000/blog/blog.id
    path('<int:blog_pk>', blog_detail, name='blog_detail'),
    path('blogtype/<int:blog_type_pk>', blogs_with_type, name='blogs_with_type'),
    path('date/<int:year>/<int:month>', blogs_with_date, name='blogs_with_date'),
]