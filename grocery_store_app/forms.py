from django.contrib.auth import forms, models
from django.core.exceptions import ValidationError
from django.forms import (CharField, DecimalField, EmailField, Form,
                          IntegerField, ModelForm, NumberInput)
from django.utils.translation import gettext_lazy as _

from .models import Product, Promotion, Review


class ProductForm(ModelForm):
    price = DecimalField(
        widget=NumberInput(attrs={'min': 0, 'step': 1.00, 'max': 99999.99}),
        label=_('price')
    )

    class Meta:
        model = Product
        fields = '__all__'


class PromotionForm(ModelForm):
    discount_amount = IntegerField(
        widget=NumberInput(attrs={'min': 0, 'step': 1, 'max': 100}),
        label=_('discount_amount')
    )

    class Meta:
        model = Promotion
        fields = '__all__'


class ReviewForm(ModelForm):
    rating = IntegerField(
        widget=NumberInput(attrs={'min': 0, 'step': 1, 'max': 5}),
        label=_('rating')
    )

    class Meta:
        model = Review
        fields = '__all__'


class RegistrationForm(forms.UserCreationForm):
    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)
    email = EmailField(max_length=200, required=True)

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AddFundsForm(Form):
    money = DecimalField(label='money', decimal_places=2, max_digits=11)

    def is_valid(self) -> bool:
        def add_error(error):
            if self.errors:
                self.errors['money'] += [error]
            else:
                self.errors['money'] = [error]

        if not super().is_valid():
            return False
        money = self.cleaned_data.get('money', None)
        if not money:
            add_error(ValidationError('an error occured, money field was not specified!'))
            return False
        if money < 0:
            add_error(ValidationError('you can only add positive amount of money!'))
            return False
        return True


# from django import forms
# from.models import Product, ClientToProduct

# class OrderForm(forms.Form):
#     product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Выберите продукт")
#     quantity = forms.IntegerField(min_value=1, label="Количество")

#     def __init__(self, *args, **kwargs):
#         super(OrderForm, self).__init__(*args, **kwargs)
#         self.fields['product'].widget.attrs.update({'onchange': 'this.form.submit();'})
