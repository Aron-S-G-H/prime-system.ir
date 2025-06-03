from apps.home_app.models import AboutUs, Information
from apps.product_app.models import GeneralCategory
from apps.cart_app.cart_module import Cart


def base_context(request):
    about_us = AboutUs.objects.last()
    information = Information.objects.last()
    general_categories = GeneralCategory.objects.all()
    cart = Cart(request)
    context = {
        'about_us': about_us,
        'information': information,
        'general_categories': general_categories,
        'cart': cart
    }
    return context
