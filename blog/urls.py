from django.urls import path 

from . import views
from .views import PostCreateView ,PostUpdateView ,PostDeleteView
app_name = 'blog'

urlpatterns = [
    path('' , views.post_list , name='post_list'),
    path('add_post/' , PostCreateView.as_view() , name='add_post'),
    path('<slug:slug>/update/', PostUpdateView.as_view(), name='update_post'),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('<slug:slug>/', views.blog_post, name='detail'),
]
