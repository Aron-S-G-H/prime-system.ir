from django.db import models
from django.contrib.auth import get_user_model
from apps.product_app.models import Product
import uuid


User = get_user_model()


class UserOrder(models.Model):
    order_uuid = models.UUIDField(editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=11)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=12, null=True, blank=True)
    address = models.TextField()
    note = models.TextField(null=True, blank=True)
    total_price = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_sms_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ('-created_at',)


class ProductOrder(models.Model):
    order = models.ForeignKey(UserOrder, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    product_unique_id = models.CharField(max_length=110)
    product_price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)
    item_total = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
