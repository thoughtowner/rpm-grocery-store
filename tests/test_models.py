from datetime import date, datetime, timedelta, timezone
from typing import Iterable

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from grocery_store_app.models import (Category, Client, Product, Promotion,
                                      Review, check_created_datetime,
                                      check_discount_amount, check_end_date,
                                      check_modified_datetime, check_money,
                                      check_price, check_quantity,
                                      check_rating, check_start_date)


current_datetime = datetime.now(tz=timezone.utc)
yesterday_datetime = current_datetime - timedelta(days=1)
tomorrow_datetime = current_datetime + timedelta(days=1)


class ClientTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='ABC', first_name='ABC', last_name='ABC', password='ABC')

    def test_invalid(self):
        with self.assertRaises(ValidationError):
            Client.objects.create(user=self.user, money=-1)

    def test_create_and_str(self):
        self.assertEqual(str(Client.objects.create(user=self.user)), 'ABC (ABC ABC)')


class CategoryStrTest(TestCase):
    """Test for category str method."""

    def test_str(self):
        self.try_save({'title': 'ABC'})

    def try_save(self, attrs):
        self.assertEqual(str(Category.objects.create(**attrs)), 'ABC')


class ProductStrTest(TestCase):
    """Test for product str method."""

    def setUp(self) -> None:
        """Set up things for tests."""
        self.category = Category.objects.create(title = 'A', description = 'ABC')

    def test_str(self):
        self.try_save({'title': 'ABC', 'price': 123.45, 'category': self.category})

    def try_save(self, attrs):
        self.assertEqual(str(Product.objects.create(**attrs)), 'ABC (123.45 RUB)')


class PromotionStrTest(TestCase):
    """Test for promotion str method."""

    def test_str(self):
        self.try_save({'title': 'ABC', 'discount_amount': 10})

    def try_save(self, attrs):
        self.assertEqual(str(Promotion.objects.create(**attrs)), f'ABC (discount amount: 10, discount time: {current_datetime.date()} - {current_datetime.date()})')


class ReviewStrTest(TestCase):
    """Test for review str method."""

    def setUp(self) -> None:
        """Set up things for tests."""
        self.category = Category.objects.create(title = 'A', description = 'ABC')
        self.product = Product.objects.create(title = 'A', price = 100.00, category = self.category)
        self.user = User.objects.create_user(username='user', password='user')
        self.client = Client.objects.create(user=self.user, money=0)

    def test_str(self):
        self.try_save({'text': 'ABC', 'product': self.product, 'client': self.client})

    def try_save(self, attrs):
        self.assertEqual(str(Review.objects.create(**attrs)), 'ABC (rating: 5/5)')


def get_valid_category_attrs() -> dict:
    return {'title': 'A', 'description': 'ABC'}

def get_invalid_category_attrs() -> tuple[dict]:
    return (
        {'title': 'ABC', 'created_datetime': tomorrow_datetime},
        {'title': 'ABC', 'modified_datetime': tomorrow_datetime},
    )

def get_valid_product_attrs(category) -> dict:
    return {'title': 'A', 'price': 100.00, 'category': category}

def get_invalid_product_attrs(category) -> tuple[dict]:
    return (
        {'title': 'ABC', 'price': 100.00, 'category': None},
        {'title': 'ABC', 'price': -100.00, 'category': category},
        {'title': 'ABC', 'price': 20000.00, 'category': category},
        {'title': 'ABC', 'price': 100.00, 'category': category, 'created_datetime': tomorrow_datetime},
        {'title': 'ABC', 'price': 100.00, 'category': category, 'modified_datetime': tomorrow_datetime},
    )

def get_valid_promotion_attrs() -> dict:
    return {'title': 'ABC', 'discount_amount': 10}

def get_invalid_promotion_attrs() -> tuple[dict]:
    return (
        {'title': 'ABC', 'discount_amount': -10},
        {'title': 'ABC', 'discount_amount': 200},
        {'title': 'ABC', 'discount_amount': 10, 'start_date': yesterday_datetime.date()},
        {'title': 'ABC', 'discount_amount': 10, 'end_date': yesterday_datetime.date()},
        {'title': 'ABC', 'discount_amount': 10, 'created_datetime': tomorrow_datetime},
        {'title': 'ABC', 'discount_amount': 10, 'modified_datetime': tomorrow_datetime},
    )

def get_valid_review_attrs(product, client) -> dict:
    return {'text': 'ABC', 'product': product, 'client': client}

def get_invalid_review_attrs(product, client) -> tuple[dict]:
    return (
        {'text': 'ABC', 'product': product, 'client': client, 'created_datetime': tomorrow_datetime},
        {'text': 'ABC', 'product': product, 'client': client, 'modified_datetime': tomorrow_datetime},
    )


class CategoryModelTest(TestCase):
    """Test for category."""

    def test_unsuccessful_creation(self):
        """Test creating attrs with invalid attrs."""
        for invalid_attrs in get_invalid_category_attrs():
            with self.assertRaises(ValidationError):
                self.try_save(invalid_attrs)

    def test_successful_creation(self):
        self.try_save(get_valid_category_attrs())

    def try_save(self, attrs):
        instance = Category(**attrs)
        instance.full_clean()
        instance.save()


class ProductModelTest(TestCase):
    """Test for product."""

    def setUp(self) -> None:
        """Set up things for tests."""
        self.category = Category.objects.create(title = 'A', description = 'ABC')

    def test_unsuccessful_creation(self):
        """Test creating attrs with invalid attrs."""
        for invalid_attrs in get_invalid_product_attrs(self.category):
            with self.assertRaises(ValidationError):
                self.try_save(invalid_attrs)

    def test_successful_creation(self):
        self.try_save(get_valid_product_attrs(self.category))

    def try_save(self, attrs):
        instance = Product(**attrs)
        instance.full_clean()
        instance.save()


class PromotionModelTest(TestCase):
    """Test for promotion."""

    def test_unsuccessful_creation(self):
        """Test creating attrs with invalid attrs."""
        for invalid_attrs in get_invalid_promotion_attrs():
            with self.assertRaises(ValidationError):
                self.try_save(invalid_attrs)

    def test_successful_creation(self):
        self.try_save(get_valid_promotion_attrs())

    def try_save(self, attrs):
        instance = Promotion(**attrs)
        instance.full_clean()
        instance.save()


class ReviewModelTest(TestCase):
    """Test for review."""

    def setUp(self) -> None:
        """Set up things for tests."""
        self.category = Category.objects.create(title = 'A', description = 'ABC')
        self.product = Product.objects.create(title = 'A', price = 100.00, category = self.category)
        self.user = User.objects.create_user(username='user', password='user')
        self.client = Client.objects.create(user=self.user, money=0)

    def test_unsuccessful_creation(self):
        """Test creating attrs with invalid attrs."""
        for invalid_attrs in get_invalid_review_attrs(self.product, self.client):
            with self.assertRaises(ValidationError):
                self.try_save(invalid_attrs)

    def test_successful_creation(self):
        self.try_save(get_valid_review_attrs(self.product, self.client))

    def try_save(self, attrs):
        instance = Review(**attrs)
        instance.full_clean()
        instance.save()


PAST = datetime(datetime.today().year-1, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)
FUTURE = datetime(datetime.today().year+1, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)

validators_pass = (
    (check_created_datetime, PAST),
    (check_modified_datetime, PAST),
    (check_start_date, FUTURE.date()),
    (check_end_date, FUTURE.date()),
    (check_price, 100),
    (check_discount_amount, 10),
    (check_money, 100),
    (check_rating, 5),
    (check_quantity, 10),
)

validators_fail = (
    (check_created_datetime, FUTURE),
    (check_modified_datetime, FUTURE),
    (check_start_date, PAST.date()),
    (check_end_date, PAST.date()),
    (check_price, -100),
    (check_discount_amount, -10),
    (check_money, -100),
    (check_rating, -5),
    (check_quantity, -10),
)

def create_val_test(validator, value, valid=True):
    def test(self):
        with self.assertRaises(ValidationError):
            validator(value)
    return lambda _ : validator(value) if valid else test

invalid_methods = {f'test_inval_{args[0].__name__}': create_val_test(*args, valid=False) for args in validators_fail}
valid_methods = {f'test_val_{args[0].__name__}': create_val_test(*args) for args in validators_pass}

ValidatorsTest = type('ValidatorsTest', (TestCase,), invalid_methods | valid_methods)
