from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='detail'),
    path('add/<int:pk>', views.CartAddView.as_view(), name='add'),
    path('remove/<str:unique_id>', views.CartRemoveView.as_view(), name='remove'),
    path('update', views.CartUpdateView.as_view(), name='update'),
    path('checkout', views.CheckOutView.as_view(), name='checkout'),
]
