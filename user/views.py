from django.shortcuts import render , redirect
from . forms import UserCreationForm , LoginForm ,UpdateUserForm , UpdateProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from blog.models import Post
from .models import Profile


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST) #Using data from request to create a new account for user
        if form.is_valid(): #To check data is valid and it is completed or not
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1']) #To clean password for anew user and save it 
            new_user.save()
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None: #If user have data from authenticate
                login(request, user)

                # To get username for message
                username = form.cleaned_data['username'] 
                messages.success(
                    request, 'تهانينا {} لقد تمت عمليه التسجيل بنجاح .'.format(username)
                )
                return redirect('user:profile')
    else:
        form = UserCreationForm()
    return render(request , 'user/signup.html' , {
        'title' : 'التسجيل',
        'form' : form,
    })


def login_user(request):
    if request.method == "POST":
        form = LoginForm() #To create "form" variable 
        username = request.POST['username'] #To import username from request
        password = request.POST['password'] #To import password from request
        user = authenticate(request ,username=username , password=password) #To login using username and password
        if user is not None: #If user have data from authenticate
            login(request, user)
            return redirect('user:profile')
        else:
            messages.warning(request, 'هناك خطأ فى اسم المستخدم او كلمه المرور .')
    else:
        form = LoginForm()
    return render(request , 'user/login.html', {
        'title' : 'تسجيل الدخول',
        'form' : form,
        
    })

def logout_user(request):
    logout(request) #To logout user
    posts = Post.objects.all() #To import all posts from blog app to appear inside my app user

    return render(request , 'user/logout.html',{
        'title' : 'تسجيل الخروج',
        'posts' : posts,

    })

@login_required(login_url='user:login') #For redirect user to login page if he want go to profile but he didn't login
def profile(request):
    user_count_posts = Post.objects.filter(author =request.user)

    paginator = Paginator(user_count_posts , 1)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request , 'user/profile.html', {
        'title' : 'الصفحه الشخصيه' ,
        'posts' : posts, 
        'user_count_posts' : user_count_posts,
    })


@login_required(login_url='user:login')
def update_profile(request):
    user_form = UpdateUserForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)

    if request.method == "POST":
        user_form = UpdateUserForm( request.POST , instance=request.user)
        profile_form = UpdateProfileForm(request.POST , request.FILES ,instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'لقد تم تعديل الملف الشخصي بنجاح .'
            )
            return redirect('user:profile')

    return render(request , 'user/edit_profile.html',{
        'title' : 'تعديل البروفيل',
        'user_form' : user_form ,
        'profile_form' : profile_form

    })

