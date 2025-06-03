from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from utils.validators import validate_convert_phone
from django.core.validators import EmailValidator
from django import forms
from django.forms import ValidationError


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = CustomUser
        fields = '__all__'


class LoginForm(forms.Form):
    phone = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'name': 'phone',
            'placeholder': 'تلفن همره',
            'class': 'form-control float-input',
            'id': 'floatingInput'
        }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'name': 'password',
            'placeholder': 'کلمه عبور',
            'class': 'form-control float-input',
            'id': 'floatingPassword'
        }
    ))

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        phone_number = validate_convert_phone(phone_number)
        return phone_number


class RegisterForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'name': 'firstName',
            'placeholder': 'نام',
            'id': 'floatingFirstName',
            'class': 'form-control float-input',
        }
    ))
    last_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'name': 'lastName',
            'placeholder': 'نام خانوادگی',
            'id': 'floatingLastName',
            'class': 'form-control float-input',
        }
    ))
    phone = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'name': 'phone',
            'placeholder': 'تلفن همره',
            'class': 'form-control float-input',
            'id': 'floatingPhone'
        }
    ))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={
            'name': 'email',
            'placeholder': 'آدرس ایمیل',
            'id': 'floatingEmail',
            'class': 'form-control float-input',
        },
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'name': 'password',
            'placeholder': 'کلمه عبور',
            'class': 'form-control float-input',
            'id': 'floatingPassword'
        }
    ))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'name': 'confirmPassword',
            'placeholder': 'تکرار کلمه عبور',
            'id': 'floatingConfirm',
            'class': 'form-control float-input',
        })
    )

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        phone_number = validate_convert_phone(phone_number)
        return phone_number

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise ValidationError('نام معتبر نمی باشد ، فقط از حروف استفاده کنید')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise ValidationError('نام خانوادگی معتبر نمی باشد ، فقط از حروف استفاده کنید')
        return last_name

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('password', 'کلمات عبور یکسان نیستند')


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'name': 'email',
            'placeholder': 'آدرس ایمیل',
            'id': 'floatingEmail',
            'class': 'form-control float-input',
        }),
        validators=[EmailValidator]
    )
