"""Admin module."""

from django.contrib import admin

from .models import (Category, Client, ClientToProduct, Product,
                     ProductToPromotion, Promotion, Review)


class ProductToPromotionInline(admin.TabularInline):
    """Add ProductToPromotion to the admin panel."""

    model = ProductToPromotion
    extra = 1


class ClientToProductInline(admin.TabularInline):
    """Add ClientToProduct to the admin panel."""

    model = ClientToProduct
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Configure the Category model in the admin panel."""


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Configure the Product model in the admin panel using inline widgets."""

    model = Product
    inlines = (ProductToPromotionInline, ClientToProductInline)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    """Configure the Promotion model in the admin panel using an inline widget."""

    model = Promotion
    inlines = (ProductToPromotionInline,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Configure the Review model in the admin panel."""

    model = Review
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Configure the Client model in the admin panel using an inline widget."""

    model = Client
    inlines = (ClientToProductInline,)
