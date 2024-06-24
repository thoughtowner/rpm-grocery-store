from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Category, Client, Product, Promotion, Review


class CategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PromotionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'


class ReviewSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ClientSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
