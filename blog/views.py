from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse
from .models import Post ,Comment
from .forms import CommentForm , CreatePostForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.generic import CreateView ,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


def post_list(request):
    posts = Post.objects.all()

    paginator = Paginator(posts , 4)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context ={
        'title' : 'الصفحه الرئيسيه',
        'posts' : posts,
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

#We use LoginRequiredMixin for no one can create blog if not login
class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post
    # fields = ['title' , 'short_description' , 'description' , 'image']
    form_class = CreatePostForm
    template_name = 'blog/add_new_post.html'

    def form_valid(self , form ):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin ,UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'blog/add_new_post.html'

    def form_valid(self , form ):
        form.instance.author = self.request.user
        return super().form_valid(form)
