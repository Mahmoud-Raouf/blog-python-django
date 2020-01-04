from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from .models import Post

def post_list(request):
    posts = Post.objects.all()

    context ={
        'title' : 'الصفحه الرئيسيه',
        'posts' : posts
    }
    return render(request ,'blog/post_list.html',context)


def blog_post(request , slug):
    post_detail = get_object_or_404(Post , slug=slug)

    context ={
        'title' : post_detail,
        'post_detail' : post_detail
    }
    return render(request ,'blog/blog-post.html',context )
