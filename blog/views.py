from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse
from .models import Post ,Comment
from .forms import CommentForm , CreatePostForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.generic import CreateView ,UpdateView ,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin
from django.db.models import Q

def post_list(request):
    posts = Post.objects.all()

    query = request.GET.get('search')
    if query:
        posts = Post.objects.filter(
        Q(title__icontains=query)|
        Q(short_description__icontains=query)|
        Q(description__icontains=query)
        )
    print(query)

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
# and should create LOGIN_URL='login' in sittings.py 
class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post
    # fields = ['title' , 'short_description' , 'description' , 'image']
    form_class = CreatePostForm
    template_name = 'blog/add_new_post.html'

    def form_valid(self , form ):
        form.instance.author = self.request.user
        return super().form_valid(form)
#ًUserPassesTestMixin = The process of verifying that this user is the owner of the post that he or she wants to Update
#and the test_func will process of this verifying
class PostUpdateView(UserPassesTestMixin , LoginRequiredMixin ,UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'blog/post_update.html'

    def form_valid(self , form ):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#ًUserPassesTestMixin = The process of verifying that this user is the owner of the post that he or she wants to delete
#and the test_func will process of this verifying
class PostDeleteView(UserPassesTestMixin , LoginRequiredMixin ,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False