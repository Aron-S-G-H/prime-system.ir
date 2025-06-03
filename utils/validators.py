from django.forms import ValidationError


persian_to_english_map = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")


def persian_to_english(number):
    """Convert Persian digits in a string to English digits."""
    return number.translate(persian_to_english_map)


def validate_convert_phone(phone_number: str) -> str:
    phone_number = phone_number.strip()  # حذف فضاهای اضافی
    phone_number = persian_to_english(phone_number)  # تبدیل ارقام فارسی به انگلیسی

    if len(phone_number) != 11:
        raise ValidationError("شماره همراه باید ۱۱ رقم باشد")

    if not phone_number.isdigit():
        raise ValidationError('شماره همراه معتبر نمی باشد')

    if not phone_number.startswith("09"):
        raise ValidationError("شماره همراه باید با ۰۹ شروع شود")

    return phone_number
