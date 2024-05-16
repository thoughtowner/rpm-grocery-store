from django import forms
from django.contrib.auth import forms as auth_forms, models as auth_models
from django.utils.translation import gettext_lazy as _

from .models import Product, Promotion, Review


class ProductForm(forms.ModelForm):
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'min': 0, 'step': 1.00, 'max': 99999.99}),
        label=_('price')
    )

    class Meta:
        model = Product
        fields = '__all__'


class PromotionForm(forms.ModelForm):
    discount_amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 0, 'step': 1, 'max': 100}),
        label=_('discount_amount')
    )

    class Meta:
        model = Promotion
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 0, 'step': 1, 'max': 5}),
        label=_('rating')
    )

    class Meta:
        model = Review
        fields = '__all__'


class RegistrationForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=200, required=True)

    class Meta:
        model = auth_models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']