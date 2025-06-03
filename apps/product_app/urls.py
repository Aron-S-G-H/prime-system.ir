from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('<str:slug>', views.ProductDetailView.as_view(), name='detail'),
    path('category/<str:slug>', views.ProductCategoryView.as_view(), name='category'),
    path('general-category/<str:slug>', views.ProductGeneralCategoryView.as_view(), name='general-category'),
    path('mobile-category-partial/<int:id>', views.mobile_category_partial, name="mobile_category_partial"),
    path('category-partial/<int:id>', views.category_partial, name='category_partial'),
]
