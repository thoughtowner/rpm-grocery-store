from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Category, Product, Promotion, Review

class CategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title', 'description',
            'created', 'modified',
        ]

class ProductSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title', 'description', 'price',
            'created', 'modified',
        ]

class PromotionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Promotion
        fields = [
            'id',
            'title', 'description', 'discount_amount',
            'start_date', 'end_date',
            'created', 'modified',
        ]

class ReviewSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'text', 'rating',
            'created', 'modified',
        ]