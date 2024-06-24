from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import client as test_client

from grocery_store_app.models import Client, Product, Category


class TestPurchase(TestCase):
    _order_page = '/order/'

    def setUp(self) -> None:
        self.test_client = test_client.Client()
        self.user = User.objects.create(username='user', password='user')
        self.grocery_store_client = Client.objects.create(user=self.user, money=0)
        self.test_client.force_login(self.user)

        product_attrs = {'title': 'A', 'price': 100.00}
        self.category = Category.objects.create(title = 'A', description = 'ABC')
        product_attrs['category'] = self.category
        self.product = Product.objects.create(**product_attrs)
        self.page_url = f'{self._order_page}?id={self.product.id}'

    def test_insufficient_funds(self):
        self.test_client.post(self.page_url, {})
        self.assertEqual(self.grocery_store_client.money, 0)
