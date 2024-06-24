from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client as TestClient
from django.urls import reverse
from rest_framework import status

from grocery_store_app.models import (Category, Client, Product, Promotion,
                                      Review)


def create_method_with_auth(url, page_name, template, login=False):
    def method(self):
        self.client = TestClient()
        if login:
            user = User.objects.create(username='user', password='user')
            Client.objects.create(user=user)
            self.client.force_login(user=user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, template)

        response = self.client.get(reverse(page_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    return method

def create_method_no_auth(url):
    def method(self):
        self.client = TestClient()
        self.assertEqual(self.client.get(url).status_code, status.HTTP_302_FOUND)
    return method

def create_method_instance(url, page_name, template, model, creation_attrs):
    def method(self):
        self.client = TestClient()
        user = User.objects.create(username='user', password='user')
        Client.objects.create(user=user)

        if model == Product:
            self.category = Category.objects.create(title = 'A', description = 'ABC')
            creation_attrs['category'] = self.category

        if model == Review:
            self.category = Category.objects.create(title = 'A', description = 'ABC')
            self.product = Product.objects.create(title = 'A', price = 100.00, category = self.category)
            self.user_ = User.objects.create_user(username='user_', password='user_')
            self.client_ = Client.objects.create(user=self.user_, money=0)
            creation_attrs['product'] = self.product
            creation_attrs['client'] = self.client_

        self.assertEqual(self.client.get(url).status_code, status.HTTP_302_FOUND)
        self.client.force_login(user=user)
        self.assertEqual(self.client.get(url).status_code, status.HTTP_302_FOUND)
        created_id = model.objects.create(**creation_attrs).id
        created_url = f'{url}?id={created_id}'
        created_reversed_url = f'{reverse(page_name)}?id={created_id}'
        response = self.client.get(created_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, template)
        self.assertEqual(self.client.get(created_reversed_url).status_code, status.HTTP_200_OK)

    return method

instance_pages = (
    ('/category/', 'category', 'entities/category.html', Category, {'title': 'A'}),
    ('/product/', 'product', 'entities/product.html', Product, {'title': 'A', 'price': 100.00}),
    ('/promotion/', 'promotion', 'entities/promotion.html', Promotion, {'title': 'A', 'discount_amount': 10}),
    ('/order/', 'order', 'pages/order.html', Product, {'title': 'A', 'price': 100.00}),
)

pages = (
    ('/categories/', 'categories', 'catalog/categories.html'),
    ('/products/', 'products', 'catalog/products.html'),
    ('/promotions/', 'promotions', 'catalog/promotions.html'),
    ('/accounts/profile/', 'profile', 'pages/profile.html'),
)

casual_pages = (
    ('', 'homepage', 'index.html'),
    ('/register/', 'register', 'registration/register.html'),
    ('/accounts/login/', 'login', 'registration/login.html'),
)

methods_with_auth = {f'test_{page[1]}': create_method_with_auth(*page, login=True) for page in pages}
TestWithAuth = type('TestWithAuth', (TestCase,), methods_with_auth)

casual_methods = {f'test_with_auth_{page[1]}': create_method_with_auth(*page, login=True) for page in casual_pages}
casual_methods.update({f'test_no_auth_{page[1]}': create_method_with_auth(*page, login=False) for page in casual_pages})
TestCasualPage = type('TestCasualPages', (TestCase,), casual_methods)

methods_no_auth = {f'test_{url}': create_method_no_auth(url) for url, _, _ in pages}
TestNoAuth = type('TestNoAuth', (TestCase,), methods_no_auth)

methods_intance = {f'test_{page[1]}': create_method_instance(*page) for page in instance_pages}
TestInstancePages = type('TestInstancePages', (TestCase,), methods_intance)
