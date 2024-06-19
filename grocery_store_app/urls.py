from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'promotions', views.PromotionViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'clients', views.ClientViewSet)

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
    path('', views.homepage, name='homepage'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('category/', views.view_category, name='category'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/', views.view_product, name='product'),
    path('promotions/', views.PromotionListView.as_view(), name='promotions'),
    path('promotion/', views.view_promotion, name='promotion'),
    path('reviews/', views.ReviewListView.as_view(), name='reviews'),
    # path('review/', views.view_review, name='review'),
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('profile/', views.profile, name='profile'),
    path('order/', views.order, name='order'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
]