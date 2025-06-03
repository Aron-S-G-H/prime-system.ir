from django.urls import path
from . import views

app_name = 'payment_gateway'

urlpatterns = [
    path('verify/<str:order_uuid>', views.verify, name='verify'),
]
