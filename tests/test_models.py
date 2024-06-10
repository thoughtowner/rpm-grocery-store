from django.test import TestCase
from typing import Iterable
from django.core.exceptions import ValidationError
from datetime import date, datetime, timezone, timedelta
from django.contrib.auth.models import User

from grocery_store_app.models import Category, Product, Promotion, Client, Review
from grocery_store_app.models import check_created_datetime, check_modified_datetime, check_start_date
from grocery_store_app.models import check_end_date, check_price, check_discount_amount, check_money, check_rating, check_quantity


def create_model_test(model_class, valid_attrs: dict, bunch_of_invalid_attrs: Iterable = None):
    class ModelTest(TestCase):
        def test_unsuccessful_creation(self):
            if bunch_of_invalid_attrs:
                for invalid_attrs in bunch_of_invalid_attrs:
                    with self.assertRaises(ValidationError):
                        model_class.objects.create(**invalid_attrs)
        
        def test_successful_creation(self):
            model_class.objects.create(**valid_attrs)
    return ModelTest

current_datetime = datetime.now(tz=timezone.utc)
yesterday_datetime = current_datetime - timedelta(days=1)
tomorrow_datetime = current_datetime + timedelta(days=1)

category_attrs = {'title': 'ABC'}
# product_attrs = {'title': 'ABC', 'price': 100.00, 'category': Category.objects.create(**category_attrs)}
product_attrs = {'title': 'ABC', 'price': 100.00}
promotion_attrs = {'title': 'ABC', 'discount_amount': 10}
review_attrs = {'text': 'ABC'}

category_invalid_attrs = (
    {'title': 'ABC', 'created_datetime': tomorrow_datetime},
    {'title': 'ABC', 'modified_datetime': tomorrow_datetime},
)

product_invalid_attrs = (
    {'title': 'ABC', 'price': -100.00},
    {'title': 'ABC', 'price': 20000.00},
    {'title': 'ABC', 'price': 100.00, 'created_datetime': tomorrow_datetime},
    {'title': 'ABC', 'price': 100.00, 'modified_datetime': tomorrow_datetime},
)

promotion_invalid_attrs = (
    {'title': 'ABC', 'discount_amount': -10},
    {'title': 'ABC', 'discount_amount': 200},
    {'title': 'ABC', 'discount_amount': 10, 'start_date': yesterday_datetime.date()},
    {'title': 'ABC', 'discount_amount': 10, 'end_date': yesterday_datetime.date()},
    {'title': 'ABC', 'discount_amount': 10, 'created_datetime': tomorrow_datetime},
    {'title': 'ABC', 'discount_amount': 10, 'modified_datetime': tomorrow_datetime},
)

review_invalid_attrs = (
    {'text': 'ABC'},
    {'text': 'ABC'},
    {'text': 'ABC', 'created_datetime': tomorrow_datetime},
    {'text': 'ABC', 'modified_datetime': tomorrow_datetime},
)

CategoryModelTest = create_model_test(Category, category_attrs, category_invalid_attrs)
ProductModelTest = create_model_test(Product, product_attrs, product_invalid_attrs)
PromotionModelTest = create_model_test(Promotion, promotion_attrs, promotion_invalid_attrs)
ReviewModelTest = create_model_test(Review, review_attrs, review_invalid_attrs)

class ClientTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='ABC', first_name='ABC', last_name='ABC', password='ABC')

    def test_invalid(self):
        with self.assertRaises(ValidationError):
            Client.objects.create(user=self.user, money=-1)

    def test_create_and_str(self):
        self.assertEqual(str(Client.objects.create(user=self.user)), 'ABC (ABC ABC)')


def create_str_test(model_class, attrs, expected_str):
    def test(self):
        self.assertEqual(str(model_class.objects.create(**attrs)), expected_str)
    return test

str_test_data = (
    # (Category, {'title': 'ABC'}, 'ABC'),
    # (Product, {'title': 'A', 'price': 123.45}, 'ABC (123.45 RUB)'),
    # (Promotion, {'title': 'ABC', 'discount_amount': 10}, f'ABC (discount amount: 10, discount time: {current_datetime.date()} - {current_datetime.date()})'),
    # (Review, {'text': 'ABC'}, 'ABC (rating 5/5)'),
)

str_methods = {f'test_{args[0].__name__}': create_str_test(*args) for args in str_test_data}
StrTest  = type('StrTest', (TestCase,), str_methods)

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

# invalid_methods = {f'test_inval_{args[0].__name__}': create_val_test(*args, valid=False) for args in validators_fail}
# valid_methods = {f'test_val_{args[0].__name__}': create_val_test(*args) for args in validators_pass}

# ValidatorsTest = type('ValidatorsTest', (TestCase,), invalid_methods | valid_methods)
