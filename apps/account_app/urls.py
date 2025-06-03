from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', views.user_logout, name='logout'),
    path('verify-register', views.VerifyRegister.as_view(), name='verify_register'),
    path('forget-password', views.ForgetPasswordView.as_view(), name='forget_password'),
    path('verify-forgot-password', views.VerifyForgetPassword.as_view(), name='verify_forget_password')
]
