from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse
from .models import Post ,Comment
from .forms import CommentForm

def post_list(request):
    posts = Post.objects.all()

    context ={
        'title' : 'الصفحه الرئيسيه',
        'posts' : posts
    }
    return render(request ,'blog/post_list.html',context)


def blog_post(request , slug):
    post_detail = get_object_or_404(Post , slug=slug)
    post = get_object_or_404(Post , slug=slug) #for import foreignkey her and select what blog we created ("post"the same fo name with model)
    posts = Post.objects.all() #for all posts in page detail
    comments = post_detail.comments.filter(active=True)

    #check before save data from comment form
    if request.method == 'POST':
        forms_comment = CommentForm(data = request.POST)
        if forms_comment.is_valid():
            new_comment = forms_comment.save(commit=False)
            new_comment.post = post
            new_comment.save()
            forms_comment = CommentForm() #have a problem here
            
    else:
        forms_comment = CommentForm()
    context ={
        'title' : post_detail,
        'post_detail' : post_detail,
        'posts' : posts,
        'comments':comments,
        'forms_comment' : forms_comment
    }


    return render(request ,'blog/blog-post.html',context )
