from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm, ForgotPasswordForm
from .models import CustomUser
from django.utils.crypto import get_random_string
from django.core.cache import cache
from .mixins import RedirectAuthenticatedMixin
from PrimeSystem.settings import LOGGER
from utils.email import send_verification_code
from utils.sms import send_otp_sms


class LoginView(RedirectAuthenticatedMixin, View):
    def get(self, request):
        context = {'login_form': LoginForm()}
        return render(request, 'account_app/login.html', context=context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(username=data['phone'], password=data['password'])
            if user:
                login(request, user)
                return JsonResponse({'status': 200, 'first_name': user.first_name, 'last_name': user.last_name})
            return JsonResponse({'status': 401})
        try:
            first_error_field, first_error_message = next(iter(login_form.errors.items()))
            error_message = first_error_message[0]  # Get the first error message for the field
        except Exception as e:
            first_error_field = 'unknown'
            error_message = f'unexpected error parsing form errors: {str(e)}'
        phone_number = request.POST.get('phone', 'unknown')
        LOGGER.warning(f'LoginView Error => {phone_number} \nfield: {first_error_field} \nmessage: {error_message} \ndata : {login_form.data.get(first_error_field)}')
        return JsonResponse({'status': 400, 'error_message': error_message})


class RegisterView(RedirectAuthenticatedMixin, View):
    def get(self, request):
        context = {'register_form': RegisterForm()}
        return render(request, 'account_app/register.html', context=context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data
            if CustomUser.objects.filter(phone=data['phone']).exists():
                register_form.add_error(None, 'کاربری با این مشخصات ثبت شده است !')
            else:
                user_data = {
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'phone': data['phone'],
                    'password': data['password'],
                }
                verification_code = get_random_string(length=5, allowed_chars='0123456789')
                send_otp_sms.apply_async(
                    (data['phone'], verification_code),
                    retry=False,
                    ignore_result=True,
                    expires=180
                )
                cache.set(verification_code, user_data, timeout=180)
                return render(request, 'account_app/send-code.html')
        try:
            first_error_field, first_error_message = next(iter(register_form.errors.items()))
            error_message = first_error_message[0]
        except Exception as e:
            first_error_field = 'unknown'
            error_message = f'unexpected error parsing form errors: {str(e)}'
        phone_number = request.POST.get('phone', 'unknown')
        LOGGER.warning(f'RegisterView Error => {phone_number} \nfield: {first_error_field} \nmessage: {error_message} \ndata: {register_form.data.get(first_error_field)}')
        return render(request, 'account_app/register.html', {'register_form': register_form})


class VerifyRegister(View):
    def post(self, request):
        code = request.POST.get('code')
        if code and code.isdigit():
            user_data = cache.get(code)
            if user_data:
                user = CustomUser.objects.create_user(
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    password=user_data['password'],
                )
                cache.delete(code)
                login(request, user)
                return JsonResponse({'status': 200, 'first_name': user.first_name, 'last_name': user.last_name})
        return JsonResponse({'status': 400, 'message': 'کد نامعتبر و یا منقضی شده است'})


class ForgetPasswordView(RedirectAuthenticatedMixin, View):
    def get(self, request):
        context = {'forget_password_form': ForgotPasswordForm()}
        return render(request, 'account_app/forget.html', context=context)

    def post(self, request):
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            user_email = forgot_password_form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=user_email)
                verification_code = get_random_string(length=5, allowed_chars='0123456789')
                send_verification_code.apply_async(
                    (verification_code, user.email),
                    retry=False,
                    ignore_result=True,
                    expires=180,
                )
                cache.set(verification_code, user.id, timeout=180)
                return render(request, 'account_app/forgot-code.html')
            except CustomUser.DoesNotExist:
                forgot_password_form.add_error('email', 'کاربری یافت نشد !')
        return render(request, 'account_app/forget.html', {'forget_password_form': forgot_password_form})


class VerifyForgetPassword(View):
    def post(self, request):
        code = request.POST.get('code')
        if code and code.isdigit():
            user_id = cache.get(code)
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                login(request, user)
                cache.delete(code)
                return JsonResponse({'status': 200, 'first_name': user.first_name, 'last_name': user.last_name})
        return JsonResponse({'status': 400, 'message': 'کد نامعتبر یا منقضی شده است'})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')
