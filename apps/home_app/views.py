from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from PrimeSystem.settings import LOGGER
from .models import SliderBanner, SmallBanner, LargeBanner, CompanyLogo
from apps.product_app.models import Category, Product, ProductAttributeValue, ProductImage
from apps.blog_app.models import BlogPost
from django.db.models import Prefetch
from django.http import JsonResponse



class HomeView(View):
    def get(self, request):
        try:
            slider_banners = SliderBanner.objects.filter(status=True)
            small_banners = SmallBanner.objects.filter(status=True).only('image', 'url').order_by('-id')[:4]
            large_banners = LargeBanner.objects.filter(status=True).only('image', 'url').order_by('-id')[:2]
            company_logos = CompanyLogo.objects.all()
            sales_products =  Product.objects.prefetch_related(
                Prefetch('attributes', queryset=ProductAttributeValue.objects.select_related('attribute').all()),
                Prefetch('images', queryset=ProductImage.objects.only('image')),
            ).filter(
                availability=True, special_price__isnull=False
            ).defer('category', 'specification', 'color')

            laptops_products = Product.objects.prefetch_related(
                'color',
                Prefetch('images', queryset=ProductImage.objects.only('image')),
            ).filter(
                availability=True, category__general_category__english_title='laptop',
            ).defer('specification', 'description', 'introduction', 'category')[:8]

            mouse_keyboards_products = Product.objects.prefetch_related(
                'color',
                Prefetch('images', queryset=ProductImage.objects.only('image')),
            ).filter(
                availability=True, category__general_category__slug='keyboardandmouse',
            ).defer('specification', 'description', 'introduction', 'category')[:8]

            categories = Category.objects.filter(icon__isnull=False).exclude(icon='').select_related('parent_category', 'general_category')
            blog_posts = BlogPost.objects.filter(publish=True).select_related('category').defer('author', 'tags', 'description', 'introduction')[:8]
            context = {
                'slider_banners': slider_banners,
                'small_banners': small_banners,
                'large_banners': large_banners,
                'company_logos': company_logos,
                'sales_products': sales_products,
                'laptops_products': laptops_products,
                'mouse_keyboards_products': mouse_keyboards_products,
                'categories': categories,
                'blog_posts': blog_posts,
            }
        except Exception as e:
            LOGGER.error("HomeView Error => \n%s", e)
            context = {}
        return render(request, 'home_app/home.html', context)


class AboutUsView(TemplateView):
    template_name = 'home_app/about-us.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    template_name = 'home_app/dashboard.html'


def countdown_end(request):
    if request.method == 'GET':
        try:
            product_id = request.GET.get('product_id')
            product = Product.objects.get(id=product_id)
            product.special_price = None
            product.special_price_time = None
            product.save()
            return JsonResponse({'status': 200, 'product_name': product.name})
        except Exception as e:
            LOGGER.error("Countdown Error => \n%s", e)
            return JsonResponse({'status': 400})
