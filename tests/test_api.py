from datetime import date, timedelta

from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from grocery_store_app.models import (Category, Client, Product,
                                      ProductToPromotion, Promotion, Review)


def create_viewset_test(model_class, url, creation_attrs):
    class ViewSetTest(TestCase):
        def setUp(self):
            self.client = APIClient()
            self.category = Category.objects.create(title = 'A', description = 'ABC')
            self.product = Product.objects.create(title = 'A', price = 100.00, category=self.category)
            self.user = User.objects.create_user(username='user', password='user')
            self.client_obj = Client.objects.create(user=self.user)
            self.superuser = User.objects.create_user(
                username='superuser', password='superuser', is_superuser=True,
            )
            self.user_token = Token.objects.create(user=self.user)
            self.superuser_token = Token.objects.create(user=self.superuser)

        def get(self, user: User, token: Token):
            self.client.force_authenticate(user=user, token=token)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_get_by_user(self):
            self.get(self.user, self.user_token)

        def test_get_by_superuser(self):
            self.get(self.superuser, self.superuser_token)

        def manage(self, user: User, token: Token, post_status: int, put_status: int, delete_status: int):
            self.client.force_authenticate(user=user, token=token)

            if model_class == Product:
                creation_attrs['category'] = self.category

            if model_class == Review:
                creation_attrs['product'] = self.product

            if model_class == Review:
                creation_attrs['client'] = self.client_obj

            created_id = model_class.objects.create(**creation_attrs).id

            if model_class == Product:
                creation_attrs['category'] = f'http://127.0.0.1:8000/rest/categories/{self.category.id}/'

            if model_class == Review:
                creation_attrs['product'] = f'http://127.0.0.1:8000/rest/products/{self.product.id}/'

            if model_class == Review:
                creation_attrs['client'] = f'http://127.0.0.1:8000/rest/clients/{self.client_obj.id}/'

            response = self.client.post(url, creation_attrs)
            self.assertEqual(response.status_code, post_status)
            response = self.client.put(f'{url}{created_id}/', creation_attrs)
            self.assertEqual(response.status_code, put_status)
            response = self.client.delete(f'{url}{created_id}/')
            self.assertEqual(response.status_code, delete_status)

        def test_manage_user(self):
            self.manage(
                self.user, self.user_token,
                post_status=status.HTTP_403_FORBIDDEN,
                put_status=status.HTTP_403_FORBIDDEN,
                delete_status=status.HTTP_403_FORBIDDEN,
            )

        def test_manage_superuser(self):
            self.manage(
                self.superuser, self.superuser_token,
                post_status=status.HTTP_201_CREATED,
                put_status=status.HTTP_200_OK,
                delete_status=status.HTTP_204_NO_CONTENT,
            )

    return ViewSetTest


CategoryViewSetTest = create_viewset_test(
    Category, '/rest/categories/',
    {'title': 'A'}
)

ProductViewSetTest = create_viewset_test(
    Product, '/rest/products/',
    {'title': 'A', 'price': 100.00}
)

PromotionViewSetTest = create_viewset_test(
    Promotion, '/rest/promotions/',
    {'title': 'A', 'discount_amount': 10}
)

ReviewViewSetTest = create_viewset_test(
    Review, '/rest/reviews/',
    {'text': 'A'}
)
