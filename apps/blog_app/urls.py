from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'blog'

urlpatterns = [
    path('', cache_page(60 * 30)(views.BlogListView.as_view()), name='list'),
    path('detail/<str:slug>', views.BlogDetailView.as_view(), name='detail'),
]
