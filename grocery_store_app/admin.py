from django.contrib import admin

from .models import (Category, Client, ClientToProduct, Product,
                     ProductToPromotion, Promotion, Review)


class ProductToPromotionInline(admin.TabularInline):
    model = ProductToPromotion
    extra = 1


class ClientToProductInline(admin.TabularInline):
    model = ClientToProduct
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = (ProductToPromotionInline, ClientToProductInline)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    model = Promotion
    inlines = (ProductToPromotionInline,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = (ClientToProductInline,)
