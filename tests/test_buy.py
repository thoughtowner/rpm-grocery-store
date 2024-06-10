from django.test import TestCase, client as test_client
from django.contrib.auth.models import User
from decimal import Decimal

from grocery_store_app.models import Client, Product

class TestPurchase(TestCase):
    _buy_page = '/buy/'

    def setUp(self) -> None:
        self.test_client = test_client.Client()
        self.user = User.objects.create(username='user', password='user')
        self.library_client = Client.objects.create(user=self.user, money=0)
        self.test_client.force_login(self.user)

        self.product = Product.objects.create(title='ABC', volume=1, price=1)
        self.page_url = f'{self._buy_page}?id={self.product.id}'

    def test_insufficient_funds(self):
        self.test_client.post(self.page_url, {})
        self.assertEqual(self.library_client.money, 0)
        self.assertNotIn(self.product, self.library_client.products.all())

    def test_purchase(self):
        self.library_client.money = 1
        self.library_client.save()

        self.test_client.post(self.page_url, {})
        self.library_client.refresh_from_db()

        self.assertEqual(self.library_client.money, 0)
        self.assertIn(self.product, self.library_client.products.all())

    def test_repeated_purchase(self):
        self.library_client.money = 2
        self.library_client.save()
        self.test_client.post(self.page_url, {})
        self.test_client.post(self.page_url, {})

        self.library_client.refresh_from_db()
        self.assertEqual(self.library_client.money, Decimal(1))
        client_products = self.library_client.products.filter(id=self.product.id)
        self.assertEqual(len(client_products), 1)
