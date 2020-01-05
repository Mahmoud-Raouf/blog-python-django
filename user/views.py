from django.shortcuts import render , redirect
from . forms import UserCreationForm
from django.contrib import messages


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
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

