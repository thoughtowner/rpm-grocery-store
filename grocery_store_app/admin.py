from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.db.models import Q
from pprint import pprint
from .models import Category, Product, Promotion, Review, Client, ProductToPromotion

# inlines

class ProductToPromotionInline(admin.TabularInline):
    model = ProductToPromotion
    extra = 1

# admins

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = (ProductToPromotionInline,)


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