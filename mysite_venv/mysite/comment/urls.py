from django.urls import path
from .views import submit_comment

urlpatterns = [
	path('submit_comment', submit_comment, name='submit_comment')
]