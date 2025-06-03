from apps.product_app.models import Product

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(CART_SESSION_ID)

        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            product = Product.objects.get(id=int(item['product_id']))
            item['product'] = product
            item['total'] = int(item['quantity']) * int(float(item['price']))
            item['unique_id'] = self.unique_id_generator(product.id, product.english_name, item['price'])
            yield item

    @staticmethod
    def unique_id_generator(product_id, product_name, product_price):
        result = f'{product_id}-{product_name}-{product_price}'
        return result

    def get_product_uniqueid(self, product):
        if product.special_price:
            return self.unique_id_generator(product.id, product.english_name, product.special_price)
        else:
            return self.unique_id_generator(product.id, product.english_name, product.base_price)

    def cart_quantity(self):
        cart = self.cart.values()
        quantity = len(cart)
        return quantity

    def total(self):
        cart = self.cart.values()
        total = sum(int(float(item['price'])) * int(item['quantity']) for item in cart)
        return total

    def add(self, product, quantity):
        unique_id = self.get_product_uniqueid(product)

        if unique_id not in self.cart:
            if product.special_price:
                self.cart[unique_id] = {
                    'quantity': 0,
                    'price': str(product.special_price),
                    'product_id': str(product.id),
                    'discount_percent': str(product.discount_percent()),
                }
            else:
                self.cart[unique_id] = {
                    'quantity': 0,
                    'price': str(product.base_price),
                    'product_id': str(product.id),
                }
        self.cart[unique_id]['quantity'] += int(quantity)
        self.save()

    def check_quantity(self, product, quantity):
        unique_id = self.get_product_uniqueid(product)
        if unique_id in self.cart:
            x = self.cart[unique_id]['quantity'] + int(quantity)
            if x > product.quantity:
                return False
            return True
        return True

    def remove_cart(self):
        del self.session[CART_SESSION_ID]

    def delete(self, unique_id):
        if unique_id in self.cart:
            del self.cart[unique_id]
            self.save()

    def save(self):
        self.session.modified = True
