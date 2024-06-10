from django.test import TestCase
from grocery_store_app.forms import RegistrationForm, AddFundsForm
from django.contrib.auth.models import User

valid_data = {
    'username': 'abc',
    'first_name': 'abc',
    'last_name': 'abc',
    'email': 'email@email.com',
    'password1': 'tArAs0ff2005',
    'password2': 'tArAs0ff2005',
}

not_matching_password = valid_data.copy()
not_matching_password['password2'] = 'abc'

invalid_email = valid_data.copy()
invalid_email['email'] = 'abc'

short_password = valid_data.copy()
short_password['password1'] = 'abc'
short_password['password2'] = 'abc'

common_password = valid_data.copy()
common_password['password1'] = 'abcdef123'
common_password['password2'] = 'abcdef123'

class TestRegistrationForm(TestCase):
    def test_valid(self):
        self.assertTrue(RegistrationForm(data=valid_data).is_valid())

    def test_not_matching_passwords(self):
        self.assertFalse(RegistrationForm(data=not_matching_password).is_valid())
        
    def test_short_password(self):
        self.assertFalse(RegistrationForm(data=short_password).is_valid())

    def test_invalid_email(self):
        self.assertFalse(RegistrationForm(data=invalid_email).is_valid())

    def test_common_password(self):
        self.assertFalse(RegistrationForm(data=common_password).is_valid())

    def test_existing_user(self):
        User.objects.create(username=valid_data['username'], password='abc')
        self.assertFalse(RegistrationForm(data=valid_data).is_valid())


class TestAddFundsForm(TestCase):
    def test_valid(self):
        self.assertTrue(AddFundsForm(data={'money': 100}).is_valid())

    def test_negative(self):
        self.assertFalse(AddFundsForm(data={'money': -100}).is_valid())

    def test_invalid_decimal_fields(self):
        self.assertFalse(AddFundsForm(data={'money': 100.123}).is_valid())

    def test_valid_decimal_fields(self):
        self.assertTrue(AddFundsForm(data={'money': 100.12}).is_valid())

    def test_invalid_max_digits(self):
        self.assertFalse(AddFundsForm(data={'money': 123456789123}).is_valid())