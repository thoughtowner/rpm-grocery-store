"""Forms module."""

from django.contrib.auth import forms, models
from django.core.exceptions import ValidationError
from django.forms import (CharField, DecimalField, EmailField, Form,
                          IntegerField, ModelForm, NumberInput)
from django.utils.translation import gettext_lazy as _

from .models import Product, Promotion, Review


class ProductForm(ModelForm):
    """Configure Product form with price field."""

    price = DecimalField(
        widget=NumberInput(attrs={'min': 0, 'step': 1.00, 'max': 99999.99}),
        label=_('price'),
    )

    class Meta:
        """Meta configuration for ProductForm."""

        model = Product
        fields = '__all__'


class PromotionForm(ModelForm):
    """Configure Promotion form with discount_amount field."""

    discount_amount = IntegerField(
        widget=NumberInput(attrs={'min': 0, 'step': 1, 'max': 100}),
        label=_('discount_amount'),
    )

    class Meta:
        """Meta configuration for PromotionForm."""

        model = Promotion
        fields = '__all__'


class ReviewForm(ModelForm):
    """Configure Review form with rating field."""

    rating = IntegerField(
        widget=NumberInput(attrs={'min': 0, 'step': 1, 'max': 5}),
        label=_('rating'),
    )

    class Meta:
        """Meta configuration for ReviewForm."""

        model = Review
        fields = '__all__'


class RegistrationForm(forms.UserCreationForm):
    """Extend UserCreationForm with additional fields."""

    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)
    email = EmailField(max_length=200, required=True)

    class Meta:
        """Meta configuration for RegistrationForm."""

        model = models.User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class AddFundsForm(Form):
    """
    Implement custom form for adding funds with validation.

    Returns:
        bool: True if the form is valid, False otherwise.
    """

    money = DecimalField(label='money', decimal_places=2, max_digits=11)

    def is_valid(self) -> bool:
        """
        Validate the form data, ensuring money is specified and positive.

        Returns:
            bool: True if the form is valid, False otherwise.
        """
        def add_error(error):
            """
            Help to add errors to the 'money' field.

            Args:
                error (str): Error message to append.
            """
            if self.errors:
                self.errors['money'].append(error)
            else:
                self.errors['money'] = [error]

        if not super().is_valid():
            return False

        money = self.cleaned_data.get('money')

        if not money:
            add_error(
                ValidationError(
                    'An error occurred, money field was not specified',
                ),
            )
            return False

        if money < 0:
            add_error(
                ValidationError(
                    'You can only add a positive amount of money',
                ),
            )
            return False

        return True
