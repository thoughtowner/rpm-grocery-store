"""Views module."""

from decimal import Decimal
from typing import Any

from django.contrib.auth import decorators, mixins
from django.core import exceptions
from django.core import paginator as django_paginator
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import ListView
from rest_framework import authentication, permissions, viewsets

from .forms import AddFundsForm, RegistrationForm
from .models import (Category, Client, ClientToProduct, Product,
                     ProductToPromotion, Promotion, Review)
from .serializers import (CategorySerializer, ClientSerializer,
                          ProductSerializer, PromotionSerializer,
                          ReviewSerializer)


def homepage(request):
    """
    Render the main page of the website.

    Args:
        request (django.http.HttpRequest): The Django HttpRequest object request.

    Returns:
        django.http.HttpResponse: An HTTP response containing HTML page.
    """
    return render(
        request,
        'index.html',
    )


class MyPermission(permissions.BasePermission):
    """Custom permission class that checks if the request method."""

    def has_permission(self, request, _):
        """
        Determine if the request should be granted permission based.

        Args:
            request (django.http.HttpRequest): The incoming HTTP request.
            _: Unused argument, typically the view instance.

        Returns:
            bool: True if the request should be granted permission, False otherwise.
        """
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return bool(request.user and request.user.is_authenticated)
        elif request.method in ('POST', 'DELETE', 'PUT'):
            return bool(request.user and request.user.is_superuser)
        return False


def create_viewset(model_class, serializer):
    """
    Dynamically creates a ModelViewSet for the specified model class and serializer.

    Args:
        model_class (django.db.models.Model): The Django model class.
        serializer (rest_framework.serializers.Serializer): The serializer class.

    Returns:
        rest_framework.viewsets.ModelViewSet: A configured ModelViewSet instance ready for use.
    """
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
    """
    Handle the registration process for new users.

    Args:
        request (django.http.HttpRequest): The incoming HTTP request.

    Returns:
        django.shortcuts.render: Renders the registration template.
    """
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
    """
    Dynamically creates a Django ListView with custom features.

    Args:
        model_class (type): The Django model class whose instances will be in the list view.
        plural_name (str): The name to use for the context variable the list of instances.
        template (str): The path to the template file to use for rendering the list view.

    Returns:
        type: A Django ListView instance configured with the specified model, template.
    """
    class CustomListView(mixins.LoginRequiredMixin, ListView):
        """A custom ListView that requires login, supports pagination context data."""

        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            """
            Retrieve the context data and adds a paginated list of all instances of the model.

            Args:
                **kwargs: Arbitrary keyword arguments.

            Returns:
                dict[str, Any]: The context data dictionary.
            """
            context = super().get_context_data(**kwargs)
            instances = model_class.objects.all()
            paginator = django_paginator.Paginator(instances, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context
    return CustomListView


CategoryListView = create_listview(
    Category, 'categories', 'catalog/categories.html',
)
ProductListView = create_listview(Product, 'products', 'catalog/products.html')
PromotionListView = create_listview(
    Promotion, 'promotions', 'catalog/promotions.html',
)
ReviewListView = create_listview(Review, 'reviews', 'catalog/reviews.html')
ClientListView = create_listview(Client, 'clients', 'catalog/clients.html')


def create_view(model_class, context_name, template, redirect_page):
    """
    Dynamically creates a view function for displaying details of a specific instance of a model.

    Args:
        model_class (type): Model class for the view.
        context_name (str): Context variable name for the model instance.
        template (str): Template path for rendering the view.
        redirect_page (str): URL pattern name for redirection on invalid conditions.

    Returns:
        callable: View function rendering the specified template with model instance details.
    """
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
            average_rating = Review.objects.filter(
                product=product).aggregate(
                average_rating=Avg('rating'))
            avg_rating = average_rating['average_rating']
            average_rating = avg_rating if avg_rating is not None else 0
            if isinstance(average_rating, int) or average_rating.is_integer():
                average_rating_rounded = int(average_rating)
            else:
                average_rating_rounded = round(average_rating, 1)
            context['average_rating'] = average_rating_rounded

            current_date = timezone.now().date()
            product_promotions = ProductToPromotion.objects.filter(
                product=product,
                promotion__start_date__lte=current_date,
                promotion__end_date__gte=current_date,
            )

            if product_promotions.exists():
                max_discount_amount = max(
                    pp.promotion.discount_amount for pp in product_promotions
                )
                discount_factor = Decimal((100 - max_discount_amount) / 100)
                price_with_max_discount = product.price * discount_factor
                context['product_promotions'] = product_promotions
                context['price_with_max_discount_amount'] = round(
                    price_with_max_discount, 2,
                )
                context['max_discount_amount'] = max_discount_amount

        return render(
            request,
            template,
            context,
        )
    return view


view_category = create_view(
    Category,
    'category',
    'entities/category.html',
    'categories',
)
view_product = create_view(
    Product,
    'product',
    'entities/product.html',
    'products',
)
view_promotion = create_view(
    Promotion,
    'promotion',
    'entities/promotion.html',
    'promotions',
)
view_review = create_view(Review, 'review', 'entities/review.html', 'reviews')


@decorators.login_required
def profile(request):
    """
    Handle deletion of a review by a logged-in user.

    Args:
        request: HttpRequest object containing the request data.

    Returns:
        HttpResponseRedirect: Redirects to the categories page if no product ID is found.
        RenderResponse: Renders the delete_review template if the request is neither GET nor POST.
        Otherwise, deletes the review and redirects to the product page.
    """
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
        {
            'product': cp.product,
            'quantity': cp.quantity,
            'price': cp.price,
        } for cp in client_products
    ]

    return render(
        request,
        'pages/profile.html',
        {
            'form': form,
            'form_errors': form_errors,
            'client_data': {
                'username': client.user.username,
                'money': client.money,
            },
            'products_with_quantities': products_with_quantities,
        },
    )


@decorators.login_required
def order(request):
    """
    Handle deletion of a review by a logged-in user.

    Args:
        request: HttpRequest object containing the request data.

    Returns:
        HttpResponseRedirect: Redirects to the categories page if no product ID is found.
        RenderResponse: Renders the delete_review template if the request is neither GET nor POST.
        Otherwise, deletes the review and redirects to the product page.
    """
    product_id = request.GET.get('id', None)
    if not product_id:
        return redirect('categories')
    try:
        product = Product.objects.get(id=product_id) if product_id else None
    except exceptions.ObjectDoesNotExist:
        return redirect('categories')
    if not product:
        return redirect('categories')

    client = Client.objects.get(user=request.user)

    if request.method == 'GET':
        price_with_max_discount_amount = Decimal(
            request.GET.get(
                'price_with_max_discount_amount',
                None,
            ).replace(',', '.'),
        )
        quantity = int(request.GET.get('quantity', None))

    if request.method == 'POST':
        price_with_max_discount_amount = Decimal(
            request.POST.get(
                'price_with_max_discount_amount',
                None,
            ).replace(',', '.'),
        )
        quantity = int(request.POST.get('quantity', None))

    sum_price_quantity = Decimal(quantity * price_with_max_discount_amount)

    if request.method == 'POST':
        if client.money >= sum_price_quantity:
            client.money -= sum_price_quantity
            client.save()
            try:
                client_to_product = ClientToProduct.objects.get(
                    client_id=client.id,
                    product_id=product_id,
                    price=price_with_max_discount_amount,
                )
                client_to_product.quantity += quantity
                client_to_product.save()
            except Exception:
                client_to_product = ClientToProduct.objects.create(
                    client_id=client.id,
                    product_id=product_id,
                    quantity=quantity,
                    price=price_with_max_discount_amount)
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
            'price_with_max_discount_amount': price_with_max_discount_amount,
        },
    )


@decorators.login_required
def cancel_order(request):
    """
    Handle deletion of a review by a logged-in user.

    Args:
        request: HttpRequest object containing the request data.

    Returns:
        HttpResponseRedirect: Redirects to the categories page if no product ID is found.
        RenderResponse: Renders the delete_review template if the request is neither GET nor POST.
        Otherwise, deletes the review and redirects to the product page.
    """
    product_id = request.GET.get('id', None)
    if not product_id:
        return redirect('categories')
    try:
        product = Product.objects.get(id=product_id) if product_id else None
    except exceptions.ObjectDoesNotExist:
        return redirect('categories')
    if not product:
        return redirect('categories')

    client = Client.objects.get(user=request.user)

    returned_quantity = int(request.session.get('returned_quantity', 0))

    if request.method == 'GET':
        item_price = Decimal(
            request.GET.get(
                'item_price',
                None,
            ).replace(',', '.'),
        )
        returned_quantity = int(request.GET.get('returned_quantity', 0))
        request.session['returned_quantity'] = returned_quantity

    if request.method == 'POST':
        item_price = Decimal(
            request.POST.get(
                'item_price',
                None,
            ).replace(',', '.'),
        )

    client_to_product = ClientToProduct.objects.get(
        client_id=client.id, product_id=product_id, price=item_price)
    if returned_quantity > client_to_product.quantity:
        returned_quantity = client_to_product.quantity

    sum_price_returned_quantity = Decimal(returned_quantity * item_price)

    if request.method == 'POST':
        client_to_product = ClientToProduct.objects.get(
            client_id=client.id, product_id=product_id, price=item_price)
        if returned_quantity < client_to_product.quantity:
            sum_price_returned_quantity = returned_quantity * client_to_product.price
            client.money += sum_price_returned_quantity
            client_to_product.quantity -= returned_quantity
            client_to_product.save()
            client.save()
        else:
            returned_quantity = client_to_product.quantity
            sum_price_returned_quantity = returned_quantity * client_to_product.price
            client.money += sum_price_returned_quantity
            client_to_product.delete()
            client.save()
        return redirect('profile')

    return render(
        request,
        'pages/cancel_order.html',
        {
            'money': client.money,
            'product': product,
            'returned_quantity': returned_quantity,
            'sum_price_returned_quantity': sum_price_returned_quantity,
            'item_price': item_price,
        },
    )


@decorators.login_required
def add_review(request):
    """
    Handle deletion of a review by a logged-in user.

    Args:
        request: HttpRequest object containing the request data.

    Returns:
        HttpResponseRedirect: Redirects to the categories page if no product ID is found.
        RenderResponse: Renders the delete_review template if the request is neither GET nor POST.
        Otherwise, deletes the review and redirects to the product page.
    """
    if request.method == 'GET':
        product_id = request.GET.get('id', None)
    if request.method == 'POST':
        product_id = request.POST.get('id', None)
    if not product_id:
        return redirect('categories')
    try:
        product = Product.objects.get(id=product_id) if product_id else None
    except exceptions.ObjectDoesNotExist:
        return redirect('categories')
    if not product:
        return redirect('categories')

    client = Client.objects.get(user=request.user)

    if request.method == 'GET':
        text = request.GET.get('text', None)
        rating = int(request.GET.get('rating', None))

    if request.method == 'POST':
        text = request.POST.get('text', None)
        rating = int(request.POST.get('rating', None))
        review = Review.objects.create(
            text=text,
            rating=rating,
            product=product,
            client=client,
        )
        review.save()
        return HttpResponseRedirect(f'/product/?id={product_id}')

    return render(
        request,
        'pages/add_review.html',
        {
            'text': text,
            'rating': rating,
            'product': product,
        },
    )


@decorators.login_required
def delete_review(request):
    """
    Handle deletion of a review by a logged-in user.

    Args:
        request: HttpRequest object containing the request data.

    Returns:
        HttpResponseRedirect: Redirects to the categories page if no product ID is found.
        RenderResponse: Renders the delete_review template if the request is neither GET nor POST.
        Otherwise, deletes the review and redirects to the product page.
    """
    if request.method == 'GET':
        product_id = request.GET.get('id', None)
    if request.method == 'POST':
        product_id = request.POST.get('id', None)
    if not product_id:
        return redirect('categories')
    try:
        product = Product.objects.get(id=product_id) if product_id else None
    except exceptions.ObjectDoesNotExist:
        return redirect('categories')
    if not product:
        return redirect('categories')

    client = Client.objects.get(user=request.user)

    if request.method == 'GET':
        text = request.GET.get('text', None)
        rating = request.GET.get('rating', None)

    if request.method == 'POST':
        text = request.POST.get('text', None)
        rating = int(request.POST.get('rating', None))
        review = Review.objects.get(
            text=text,
            rating=rating,
            product=product,
            client=client,
        )
        review.delete()
        return HttpResponseRedirect(f'/product/?id={product_id}')

    return render(
        request,
        'pages/delete_review.html',
        {
            'text': text,
            'rating': rating,
            'product': product,
        },
    )
