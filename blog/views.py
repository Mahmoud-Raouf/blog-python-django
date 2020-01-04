from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from .models import Post ,Comment

def post_list(request):
    posts = Post.objects.all()

    context ={
        'title' : 'الصفحه الرئيسيه',
        'posts' : posts
    }
    return render(request ,'blog/post_list.html',context)


def blog_post(request , slug):
    post_detail = get_object_or_404(Post , slug=slug)
    posts = Post.objects.all()
    comments = post_detail.comments.filter(active=True)

    context ={
        'title' : post_detail,
        'post_detail' : post_detail,
        'posts' : posts,
        'comments':comments
    }
    return render(request ,'blog/blog-post.html',context )
