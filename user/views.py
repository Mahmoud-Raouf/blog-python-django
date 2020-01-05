from django.shortcuts import render , redirect
from . forms import UserCreationForm , LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST) #Using data from request to create a new account for user
        if form.is_valid(): #To check data is valid and it is completed or not
            form.save()
            username = form.cleaned_data['username'] # To get username for message
            messages.success(
                request, 'تهانينا {} لقد تمت عمليه التسجيل بنجاح .'.format(username)
            )
            return redirect('/blog/')
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
            return redirect('/blog')
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
    return render(request , 'user/logout.html',{
        'title' : 'تسجيل الخروج',
    })


def profile(request):
    return render(request , 'user/profile.html', {
        'title' : 'الصفحه الشخصيه' ,
    })