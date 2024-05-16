from django.contrib import admin

from .models import Category, Product, Promotion, Review, Client, CategoryToCategory, ProductToPromotion

# inlines

class CategoryToCategoryInline(admin.TabularInline):
    model = CategoryToCategory
    extra = 1
    fk_name = 'parent_category'


class ProductToPromotionInline(admin.TabularInline):
    model = ProductToPromotion
    extra = 1

# admins

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    inlines = (CategoryToCategoryInline,)


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


@admin.register(CategoryToCategory)
class CategoryToCategoryAdmin(admin.ModelAdmin):
    model = CategoryToCategory


@admin.register(ProductToPromotion)
class ProductToPromotionAdmin(admin.ModelAdmin):
    model = ProductToPromotion


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client