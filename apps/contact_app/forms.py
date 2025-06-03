from django import forms


class ContactUsForm(forms.Form):
    message = forms.CharField(
        required=True,
        max_length=300,
        min_length=10,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Leave a comment here',
                'rows': '5',
                'class': 'form-control',
                'id': 'floatingTextarea2',
                'style': 'height: 150px;'
            }
        ),
        error_messages={
            'required': 'تیکت نمیتواند شامل پیام خالی باشد',
            'max_length': 'پیام نمیتواند بیشتر از ۳۰۰ کاراکتر باشد',
            'min_length': 'پیام باید حداقل ۱۰ کاراکتر و حداکثر ۳۰۰ کاراکتر باشد'
        },
    )

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if not message:
            raise forms.ValidationError("تیکت نمیتواند شامل پیام خالی باشذ")
        return message
