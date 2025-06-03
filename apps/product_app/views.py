from django.shortcuts import render
from django.views.generic import View
from PrimeSystem.settings import LOGGER
from .models import Category, Product, ProductComment, ProductImage
from hitcount.views import HitCountDetailView
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
import random
import json


class ProductDetailView(HitCountDetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_app/product-detail.html'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = Product.objects.get(slug=self.kwargs['slug'])
        list_similar_products = list(
            Product.objects
            .prefetch_related(
                'color',
                Prefetch('images', queryset=ProductImage.objects.only('image')),
            )
            .filter(availability=True, second_hand=product.second_hand, category__general_category=product.category.general_category)
            .exclude(slug=product.slug)
            .defer('introduction', 'description', 'specification', 'category')
        )
        len_list = len(list_similar_products)
        num_similar_products = 8 if len_list > 8 else len_list
        random_products = random.sample(list_similar_products, k=num_similar_products)
        context['similar_products'] = random_products
        context['range'] = range(1, 6)
        return context

    def post(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return JsonResponse({'status': 400, 'error_message': 'خطا در دریافت محصول مربوطه'})

        try:
            data = json.loads(request.body)
            text = data.get('text', '').strip()
            rating = int(data.get('rating'))
            positive_value = data.get('positiveValue', [])
            negative_value = data.get('negativeValue', [])
            if not text:
                return JsonResponse({'status': 400, 'error_message': 'متن نظر الزامی است'})
            if not (0 <= rating <= 5):
                return JsonResponse({'status': 400, 'error_message': 'مقدار امتیاز باید بین ۰ و ۵ باشد'})
            comment = ProductComment.objects.create(product=product, user=request.user, text=text, rating=rating)
            if positive_value:
                comment.speciality = {'نقاط قوت': positive_value}
            if negative_value:
                comment.speciality = {'نقاط ضعف': negative_value}
            comment.save()
            return JsonResponse({'status': 200})
        except (ValueError, json.JSONDecodeError) as e:
            LOGGER.error("ProductDetailView Error => \n%s", e)
            return JsonResponse({'status': 400, 'error_message': 'داده‌های ارسال شده نامعتبر هستند'})


class BaseProductView(View):
    def get(self, request, slug):
        exist_check = request.GET.get('existCheck', '').lower() == 'true'
        second_hand = request.GET.get('secondHand', '').lower() == 'true'
        range_price = request.GET.get('range')
        page_number = request.GET.get('page', 1)

        # Get products based on subclass implementation
        products = self.get_products(slug)
        products = self.apply_filters(products, exist_check, second_hand, range_price)

        if not products.exists():
            return render(request, 'product_app/no-product.html')

        paginator = Paginator(products, 9)
        products_list = paginator.get_page(page_number)

        context = {'products': products_list}
        return render(request, 'product_app/products.html', context)

    def get_products(self, slug):
        raise NotImplementedError("Subclasses must implement `get_products` method.")

    def apply_filters(self, products, exist_check, second_hand, range_price):
        if exist_check:
            products = products.filter(availability=True)
        if second_hand:
            products = products.filter(second_hand=True)
        if range_price:
            min_price, max_price = map(int, range_price.split(','))
            products = products.filter(base_price__gte=min_price, base_price__lt=max_price)
        return products


class ProductListView(View):
    def get(self, request):
        search_query = request.GET.get('search')
        exist_check = request.GET.get('existCheck', '').lower() == 'true'
        second_hand = request.GET.get('secondHand', '').lower() == 'true'
        range_price = request.GET.get('range')
        page_number = request.GET.get('page', 1)

        products = Product.objects.prefetch_related(
            'color',
            Prefetch('images', queryset=ProductImage.objects.only('image')),
        ).defer(
            'description', 'specification', 'introduction', 'category',
        ).order_by(
            '-availability', 'disable_order',
        )
        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(english_name__icontains=search_query))
        if exist_check:
            products = products.filter(availability=True)
        if second_hand:
            products = products.filter(second_hand=True)
        if range_price:
            min_price, max_price = map(int, range_price.split(','))
            products = products.filter(base_price__gte=min_price, base_price__lt=max_price)
        if not products:
            return render(request, 'product_app/no-product.html')

        paginator = Paginator(products, 9)
        products_list = paginator.get_page(page_number)
        context = {'products': products_list, 'search_query': search_query}
        return render(request, 'product_app/products.html', context)


class ProductCategoryView(BaseProductView):
    def get_products(self, slug):
        return Product.objects.filter(
            Q(category__slug=slug) | Q(category__parent_category__slug=slug)
        ).prefetch_related(
            'color',
            Prefetch('images', queryset=ProductImage.objects.only('image')),
        ).defer(
            'description', 'specification', 'introduction', 'category'
        ).order_by('-availability', 'disable_order')


class ProductGeneralCategoryView(BaseProductView):
    def get_products(self, slug):
        return Product.objects.filter(
            category__general_category__slug=slug
        ).prefetch_related(
            'color',
            Prefetch('images', queryset=ProductImage.objects.only('image')),
        ).defer(
            'description', 'specification', 'introduction', 'category'
        ).order_by('-availability', 'disable_order')


def mobile_category_partial(request, category_id):
    categories = Category.objects.filter(general_category_id=category_id).only('title', 'slug')
    context = {'categories': categories}
    return render(request, 'templates/includes/mobile_category.html', context)


def category_partial(request, category_id):
    categories = Category.objects.filter(general_category_id=category_id).only('title', 'slug')
    context = {'categories': categories}
    return render(request, 'templates/includes/category.html', context)
