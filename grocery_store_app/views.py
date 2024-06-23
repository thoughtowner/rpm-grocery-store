from typing import Any

from django.contrib.auth import decorators, mixins
from django.core import exceptions
from django.core import paginator as django_paginator
from django.db.models import Avg
from django.shortcuts import redirect, render
from django.views.generic import ListView
from rest_framework import authentication, permissions, viewsets

from .forms import AddFundsForm, RegistrationForm
from .models import Category, Client, Product, Promotion, Review, ClientToProduct
from .serializers import (CategorySerializer, ClientSerializer,
                          ProductSerializer, PromotionSerializer,
                          ReviewSerializer)
from django.db.models import Prefetch


# def homepage(request):
#     client = Client.objects.get(user=request.user)
#     client_products = ClientToProduct.objects.filter(client=client).values_list('product', flat=True)
#     products = Product.objects.filter(id__in=list(client_products))
#     return render(
#         request,
#         'index.html',
#         {
#             'products': products,
#             'client_products': client_products
#         }
#     )


def homepage(request):
    return render(
        request,
        'index.html',
    )

class MyPermission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return bool(request.user and request.user.is_authenticated)
        elif request.method in ('POST', 'DELETE', 'PUT'):
            return bool(request.user and request.user.is_superuser)
        return False

def create_viewset(model_class, serializer):
    class ViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serializer
        authentication_classes = [authentication.TokenAuthentication]
        permission_classes = [MyPermission]
    return ViewSet

CategoryViewSet = create_viewset(Category, CategorySerializer)
ProductViewSet = create_viewset(Product, ProductSerializer)
PromotionViewSet = create_viewset(Promotion, PromotionSerializer)
ReviewViewSet = create_viewset(Review, ReviewSerializer)
ClientViewSet = create_viewset(Client, ClientSerializer)

def register(request):
    errors = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            return redirect('homepage')
        else:
            errors = form.errors
    else:
        form = RegistrationForm()
    return render(
        request,
        'registration/register.html',
        {'form': form, 'errors': errors},
    )

def create_listview(model_class, plural_name, template):
    class CustomListView(mixins.LoginRequiredMixin, ListView):
        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            instances = model_class.objects.all()
            paginator = django_paginator.Paginator(instances, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context
    return CustomListView

CategoryListView = create_listview(Category, 'categories', 'catalog/categories.html')
ProductListView = create_listview(Product, 'products', 'catalog/products.html')
PromotionListView = create_listview(Promotion, 'promotions', 'catalog/promotions.html')
ReviewListView = create_listview(Review, 'reviews', 'catalog/reviews.html')
ClientListView = create_listview(Client, 'clients', 'catalog/clients.html')

def create_view(model_class, context_name, template, redirect_page):
    @decorators.login_required
    def view(request):
        id_ = request.GET.get('id', None)
        if not id_:
            return redirect(redirect_page)
        try:
            target = model_class.objects.get(id=id_) if id_ else None
        except exceptions.ValidationError:
            return redirect(redirect_page)
        context = {context_name: target}
        if model_class == Product:
            try:
                product = Product.objects.get(id=id_)
            except Product.DoesNotExist:
                return None
            average_rating = Review.objects.filter(product=product).aggregate(average_rating=Avg('rating'))
            average_rating = average_rating['average_rating'] if average_rating['average_rating'] is not None else 0
            if isinstance(average_rating, int) or average_rating.is_integer():
                average_rating_rounded = int(average_rating)
            else:
                average_rating_rounded = round(average_rating, 1)
            context['average_rating'] = average_rating_rounded
        return render(
            request,
            template,
            context,
        )
    return view

view_category = create_view(Category, 'category', 'entities/category.html', 'categories')
view_product = create_view(Product, 'product', 'entities/product.html', 'products')
view_promotion = create_view(Promotion, 'promotion', 'entities/promotion.html', 'promotions')
view_review = create_view(Review, 'review', 'entities/review.html', 'reviews')


# @decorators.login_required
# def profile(request):
#     form_errors = ''
#     client = Client.objects.get(user=request.user)
#     if request.method == 'POST':
#         form = AddFundsForm(request.POST)
#         if form.is_valid():
#             money = form.cleaned_data.get('money')
#             client.money += money
#             client.save()
#     else:
#         form = AddFundsForm()

#     return render(
#         request,
#         'pages/profile.html',
#         {
#             'form': form,
#             'form_errors': form_errors,
#             'client_data': {'username': client.user.username, 'money': client.money},
#             'client_products': client.products.all(),
#         }
#     )


@decorators.login_required
def profile(request):
    form_errors = ''
    client = Client.objects.get(user=request.user)
    if request.method == 'POST':
        form = AddFundsForm(request.POST)
        if form.is_valid():
            money = form.cleaned_data.get('money')
            client.money += money
            client.save()
    else:
        form = AddFundsForm()

    client_products = ClientToProduct.objects.filter(client=client)

    products_with_quantities = [
        {'product': cp.product, 'quantity': cp.quantity} for cp in client_products
    ]

    return render(
        request,
        'pages/profile.html',
        {
            'form': form,
            'form_errors': form_errors,
            'client_data': {'username': client.user.username, 'money': client.money},
            'products_with_quantities': products_with_quantities,
        }
    )



from django.contrib.sessions.models import Session

@decorators.login_required
def order(request):
    product_id = request.GET.get('id', None)
    if not product_id:
        return redirect('products')
    try:
        product = Product.objects.get(id=product_id) if product_id else None
    except exceptions.ObjectDoesNotExist:
        return redirect('products')
    if not product:
        return redirect('products')

    client = Client.objects.get(user=request.user)

    quantity = int(request.session.get('quantity', 0))

    if request.method == 'GET' and 'quantity' in request.GET:
        quantity = int(request.GET.get('quantity', 0))
        request.session['quantity'] = quantity
    
    sum_price_quantity = quantity * product.price

    if request.method == 'POST':
        if client.money >= quantity * product.price:            
            client.money -= quantity * product.price
            client.save()
            try:
                client_to_product = ClientToProduct.objects.get(client_id=client.id, product_id=product_id)
                client_to_product.quantity += quantity
                client_to_product.save()
            except:
                client_to_product = ClientToProduct.objects.create(client_id=client.id, product_id=product_id, quantity=quantity)
                client_to_product.save()
        return redirect('profile')

    return render(
        request,
        'pages/order.html',
        {
            'money': client.money,
            'product': product,
            'quantity': quantity,
            'sum_price_quantity': sum_price_quantity,
        }
    )
