"""Serializers module."""

from rest_framework.serializers import HyperlinkedModelSerializer

from.models import Category, Client, Product, Promotion, Review


class CategorySerializer(HyperlinkedModelSerializer):
    """Serializer for the Category model."""

    class Meta:
        """Meta class for serializer."""

        model = Category
        fields = '__all__'


class ProductSerializer(HyperlinkedModelSerializer):
    """Serializer for the Category model."""

    class Meta:
        """Meta class for serializer."""

        model = Product
        fields = '__all__'


class PromotionSerializer(HyperlinkedModelSerializer):
    """Serializer for the Category model."""

    class Meta:
        """Meta class for serializer."""

        model = Promotion
        fields = '__all__'


class ReviewSerializer(HyperlinkedModelSerializer):
    """Serializer for the Category model."""

    class Meta:
        """Meta class for serializer."""

        model = Review
        fields = '__all__'


class ClientSerializer(HyperlinkedModelSerializer):
    """Serializer for the Category model."""

    class Meta:
        """Meta class for serializer."""

        model = Client
        fields = '__all__'
