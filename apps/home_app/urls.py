from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='Home_page'),
    path('about-us', cache_page(60 * 30)(views.AboutUsView.as_view()), name='AboutUs_Page'),
    path('dashboard', views.DashboardView.as_view(), name='Dashboard_Page'),
    path('countdown-end', views.countdown_end, name='countdown_end'),
]
