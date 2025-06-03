from django import forms
from utils.validators import validate_convert_phone
from .models import UserOrder


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = UserOrder
        exclude = ('user', 'total_price', 'is_paid', 'created_at')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'نام',
                'class': 'form-control float-input',
                'name': 'name',
                'id': 'floatingInputFname',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'نام خانوادگی',
                'class': 'form-control float-input',
                'name': 'lastname',
                'id': 'floatingInputLname',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'آدرس ایمیل (اختیاری)',
                'class': 'form-control float-input text-start',
                'name': 'email',
                'id': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'شماره تلفن همراه',
                'class': 'form-control float-input',
                'name': 'phone',
                'id': 'phone',
            }),
            'state': forms.TextInput(attrs={
                'placeholder': 'استان',
                'class': 'form-control float-input',
                'name': 'state',
                'id': 'state',
            }),
            'postal_code': forms.TextInput(attrs={
                'placeholder': 'کد پستی',
                'class': 'form-control float-input',
                'name': 'postal_code',
                'id': 'postal_code',
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'آدرس خود را کامل وارد کنید',
                'class': 'form-control float-input',
                'name': 'address',
                'id': 'floatingInputStreet',
            }),
            'note': forms.Textarea(attrs={
                'placeholder': 'نکاتی درباره سفارش را که لازم است یادداشت کنید',
                'class': 'form-control float-input',
                'name': 'message',
                'id': 'floatingInputDesc',
            }),
        }

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        phone_number = validate_convert_phone(phone_number)
        return phone_number

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if postal_code and not postal_code.isdigit():
            raise forms.ValidationError('کد پستی معتبر نمی باشد')
        return postal_code
