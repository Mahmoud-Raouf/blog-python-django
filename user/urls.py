from django.urls import path 
from .import views
app_name = 'blog'

urlpatterns = [
    path('signup/' , views.signup , name='signup'),
    path('login/' , views.login_user , name='login'),
    path('logout/' , views.logout_user , name='logout'),
    path('profile/' , views.profile , name='profile'),

    # # easy way "LoginView" to create login and logout using django 
    # from django.contrib.auth.views import LoginView , LogoutView
    # path('login/' , LoginView.as_view(template_name=('user/login.html')) , name='login'),
    # path('logout/' , LogoutView.as_view() , name='logout')

]
