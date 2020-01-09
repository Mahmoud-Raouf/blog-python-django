from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label='الاسم ', max_length=30, help_text='يجب الا يحتوى الاسم على مسافات')
    email = forms.EmailField(label= 'البريد الاليكترونى ')
    first_name = forms.CharField(label='الاسم الاول ')
    last_name = forms.CharField(label='الاسم الاخير ')
    who_i = forms.CharField(label='السيره الذاتيه ', max_length=150)
    password1 = forms.CharField(label='كلمه السر ', widget= forms.PasswordInput(), min_length=8) #we using widget for hidden password
    password2 = forms.CharField(label='تأكيد كلمه السر ', widget= forms.PasswordInput(), min_length=8)
    class Meta:
        model = User
        fields = ('username' , 'email' , 'first_name' , 'last_name' , 'password1', 'password2' , 'who_i')


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('كلمه السر غير متطابقه .')
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username = cd['username']).exists():
            raise forms.ValidationError('هذا الاسم موجد حاليا ادخل اسم اخر .')
        return cd['username']

class LoginForm(forms.ModelForm):
    username = forms.CharField(label='الاسم ')
    password = forms.CharField(label='كلمه السر ', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username' , 'password')


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(label='الاسم الاول ')
    last_name = forms.CharField(label='الاسم الاخير ')
    email = forms.EmailField(label= 'البريد الاليكترونى ')
    class Meta:
        model = User
        fields = ('first_name' , 'last_name' , 'email')

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image' , 'country' , 'address' , 'who_i')