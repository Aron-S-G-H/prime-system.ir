from PrimeSystem.settings import LOGGER
from django.shortcuts import render, redirect, get_object_or_404
from .cart_module import Cart
from django.http import JsonResponse
from apps.product_app.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
from django.views.generic import TemplateView, View
import json
from utils.encrypt_data import encrypt_data
from django.core.cache import cache
from .models import UserOrder, ProductOrder


class CartDetailView(TemplateView):
    template_name = 'cart_app/cart.html'


class CartAddView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        cart = Cart(request)
        quantity = 1
        if cart.check_quantity(product, quantity):
            cart.add(product, quantity)
        return redirect('cart:detail')

    def post(self, request, pk):
        quantity = request.POST.get('quantity')
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return JsonResponse({'status': 404})
        cart = Cart(request)
        if int(quantity) > product.quantity or not cart.check_quantity(product, quantity):
            return JsonResponse({'status': 400})
        cart.add(product, quantity)
        return JsonResponse({'status': 200})


class CartRemoveView(View):
    def get(self, request, unique_id):
        cart = Cart(request)
        cart.delete(unique_id)
        return JsonResponse({'status': 200})


class CartUpdateView(View):
    def post(self, request):
        update_quantity_list = request.POST.get('data')
        update_quantity_list = json.loads(update_quantity_list)
        cart = Cart(request)
        for unique_id in update_quantity_list:
            if unique_id in cart.cart:
                product = cart.cart[unique_id]
                if int(update_quantity_list[unique_id]) > Product.objects.get(id=int(product['product_id'])).quantity:
                    return JsonResponse({'status': 400})
                else:
                    product['quantity'] = int(update_quantity_list[unique_id])
        cart.save()
        return JsonResponse({'status': 200})


class CheckOutView(LoginRequiredMixin, View):
    login_url = '/accounts/login'

    def get(self, request):
        cart = Cart(request)
        if cart.cart_quantity() == 0:
            return redirect('cart:detail')
        form = CheckoutForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': request.user.phone,
        })
        return render(request, 'cart_app/checkout.html', {'form': form})

    def post(self, request):
        cart = Cart(request)
        form = CheckoutForm(request.POST)
        phone_number = request.user.phone
        user_full_name = request.user.get_full_name()
        if form.is_valid():
            data = form.cleaned_data
            order = UserOrder.objects.create(
                user=request.user,
                total_price=cart.total(),
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone=data['phone'],
                state=data['state'],
                postal_code=data['postal_code'],
                address=data['address'],
                note=data['note'],
            )
            for item in cart:
                ProductOrder.objects.create(
                    order=order,
                    product=item['product'],
                    product_unique_id=item['unique_id'],
                    product_price=item['price'],
                    quantity=item['quantity'],
                    item_total=item['total'],
                )

            order_uuid = str(order.order_uuid)
            order_id = order.id
            cache.set(order_uuid, order_id, timeout=600)
            amount = f'{cart.total()}0'
            data = {'amount': amount, 'order_id': order_id}
            context = {
                'order_uuid': order_uuid,
                'data': encrypt_data(data),
            }
            cart.remove_cart()
            LOGGER.warning(f'Redirecting to paymentGateway => \nOrderID: {order_id} \nUser: {phone_number} - {user_full_name}')
            return render(request, 'cart_app/redirect_to_payment.html', context)
        errors = {field: error for field, errors in form.errors.items() for error in errors}
        field = list(errors.keys())[0]
        error_message = list(errors.values())[0]
        LOGGER.warning(f'CheckOutView Error => \nUser: {phone_number} - {user_full_name} \nfield: {field} \nmessage: {error_message} \ndata: {request.POST.get(field)}')
        return render(request, 'cart_app/checkout.html', {'form': form, 'error_message': error_message, 'field': field})
