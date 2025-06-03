from rest_framework import serializers
from .models import Product
from collections import OrderedDict


class ProductSerializer(serializers.ModelSerializer):
    page_unique = serializers.CharField(source='id')
    title = serializers.CharField(source='name')
    subtitle = serializers.CharField(source='english_name')
    page_url = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()
    old_price = serializers.SerializerMethodField()
    image_links = serializers.SerializerMethodField(source='images')
    image_link = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    spec = serializers.SerializerMethodField()

    def to_representation(self, instance):
        # this function will remove keys that have None value
        result = super(ProductSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

    class Meta:
        model = Product
        fields = [
            'page_unique', 'title', 'subtitle', 'page_url', 'current_price',
            'availability', 'old_price', 'image_links', 'image_link', 'category_name', 'spec'
        ]

    def get_image_link(self, obj):
        request = self.context.get('request')
        image = obj.images.first()
        return request.build_absolute_uri(image.image.url).replace('http://', 'https://')

    def get_image_links(self, obj):
        request = self.context.get('request')
        images = obj.images.all()
        images_url = []
        for image in images:
            absolute_url = request.build_absolute_uri(image.image.url).replace('http://', 'https://')
            images_url.append(absolute_url)
        return images_url

    def get_current_price(self, obj):
        if obj.special_price:
            price = obj.special_price
        else:
            price = obj.base_price
        return price

    def get_old_price(self, obj):
        if obj.special_price:
            old_price = obj.base_price
            return old_price
        return None

    def get_availability(self, obj):
        if obj.availability:
            availability = 'instock'
        else:
            availability = 'outofstock'
        return availability

    def get_category_name(self, obj):
        category_name = obj.category.title
        return category_name

    def get_page_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url()).replace('http://', 'https://')

    def get_spec(self, obj):
        return {attr.attribute.name: attr.value for attr in obj.attributes.all()}
