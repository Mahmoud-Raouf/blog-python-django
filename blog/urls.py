from django.urls import path 

from . import views
from .views import PostCreateView
app_name = 'blog'

urlpatterns = [
    path('' , views.post_list , name='post_list'),
    path('add_post/' , PostCreateView.as_view() , name='add_post'),
    path('<slug:slug>/', views.blog_post, name='detail'),
]
