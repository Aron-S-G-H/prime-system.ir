from .serializers import ProductSerializer
from rest_framework.views import APIView
from .pagination import CustomPagination
from.models import Product
from urllib.parse import urlparse


class ProductApi(APIView):
    def post(self, request):
        page_unique = request.data.get('page_unique', None)
        page_url = request.data.get('page_url', None)
        if page_unique:
            products = Product.objects.filter(id=page_unique)
        elif page_url:
            parsed_url = urlparse(page_url)
            product_slug = parsed_url.path.split('/')[-1]
            products = Product.objects.filter(slug=product_slug)
        else:
            products = Product.objects.prefetch_related('images', 'attributes').all().order_by('-update_at')
        paginator = CustomPagination()
        result = paginator.paginate_queryset(queryset=products, request=request)
        serializer = ProductSerializer(instance=result, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
