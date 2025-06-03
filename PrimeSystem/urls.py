from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from PrimeSystem import settings
from .views import robots
from apps.product_app.sitemaps import ProductSiteMap
from apps.blog_app.sitemaps import BlogSiteMap
from apps.home_app.sitemaps import StaticSiteMap, FaviconSitemap
from django.contrib.sitemaps.views import sitemap
from apps.product_app.api import ProductApi


sitemaps = {
    'products': ProductSiteMap,
    'blogs': BlogSiteMap,
    'static': StaticSiteMap,
    "favicon": FaviconSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home_app.urls')),
    path('accounts/', include('apps.account_app.urls')),
    path('blogs/', include('apps.blog_app.urls')),
    path('products/', include('apps.product_app.urls')),
    path('cart/', include('apps.cart_app.urls')),
    path('contact-us/', include('apps.contact_app.urls')),
    path('payment-gateway/', include('apps.paymentGateway_app.urls')),
    path('api/torob/products/', ProductApi.as_view(), name='product_api'),
    path('api/torob/products', ProductApi.as_view(), name='product_api'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('robots.txt', robots, name="robots"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "PrimeSystem.views.page_not_found_view"
