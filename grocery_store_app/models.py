"""Models modul."""

from datetime import date, datetime, timezone
from typing import Any
from uuid import uuid4

from django.conf.global_settings import AUTH_USER_MODEL
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

CATEGORY_TITLE_MAX_LENGTH = 100
CATEGORY_DESCRIPTION_MAX_LENGTH = 1000
PRODUCT_TITLE_MAX_LENGTH = 200
PRODUCT_DESCRIPTION_MAX_LENGTH = 2000
PROMOTION_TITLE_MAX_LENGTH = 200
PROMOTION_DESCRIPTION_MAX_LENGTH = 2000
REVIEW_TEXT_MAX_LENGTH = 1000
DEFAULT_IMAGE = 'https://acropora.ru/images/yootheme/pages/features/panel03.jpg'


def get_current_datetime() -> datetime:
    """
    Get the current datetime in UTC.

    Returns:
        datetime: Current datetime in UTC.
    """
    return datetime.now(tz=timezone.utc)


def get_current_date() -> date:
    """
    Get the current date.

    Returns:
        date: Current date.
    """
    return date.today()


def check_created_datetime(created_datetime: datetime) -> None:
    """
    Validate that created_datetime is not in the future.

    Args:
        created_datetime (datetime): Datetime to validate.

    Raises:
        ValidationError: If created_datetime is in the future.
    """
    if created_datetime > get_current_datetime():
        raise ValidationError(
            _('The created datetime should be less than or equal to the current datetime'),
            params={'created_datetime': created_datetime})


def check_modified_datetime(modified_datetime: datetime) -> None:
    """
    Validate that modified_datetime is not in the future.

    Args:
        modified_datetime (datetime): Datetime to validate.

    Raises:
        ValidationError: If modified_datetime is in the future.
    """
    if modified_datetime > get_current_datetime():
        raise ValidationError(
            _('The modified datetime should be less than or equal to the current datetime'),
            params={'modified_datetime': modified_datetime})


def check_start_date(start_date: date) -> None:
    """
    Validate that start_date is not in the past.

    Args:
        start_date (date): Date to validate.

    Raises:
        ValidationError: If start_date is in the past.
    """
    if start_date < get_current_date():
        raise ValidationError(
            _('The start date should be greater than or equal to the current date'),
            params={'start_date': start_date},
        )


def check_end_date(end_date: date) -> None:
    """
    Validate that end_date is not in the past.

    Args:
        end_date (date): Date to validate.

    Raises:
        ValidationError: If end_date is in the past.
    """
    if end_date < get_current_date():
        raise ValidationError(
            _('The end date should be greater than or equal to the current date'),
            params={'end_date': end_date},
        )


def check_price(price: int | float) -> None:
    """
    Validate that price is within the allowed range.

    Args:
        price (int | float): Price to validate.

    Raises:
        ValidationError: If price is out of range.
    """
    if price <= 0 or price >= 10000:
        raise ValidationError(
            _('The price should be in the range between 0.01 and 9999.99 inclusive'),
            params={'price': price},
        )


def check_discount_amount(discount_amount: int) -> None:
    """
    Validate that discount_amount is within the allowed range.

    Args:
        discount_amount (int): Discount amount to validate.

    Raises:
        ValidationError: If discount_amount is out of range.
    """
    if discount_amount < 0 or discount_amount > 100:
        raise ValidationError(
            _('The discount amount should be in the range between 0 and 100 inclusive'),
            params={'discount_amount': discount_amount},
        )


def check_money(money: int | float) -> None:
    """
    Validate that money is within the allowed range.

    Args:
        money (int | float): Money to validate.

    Raises:
        ValidationError: If money is out of range.
    """
    if money < 0 or money >= 10000000:
        raise ValidationError(
            _('The money should be in the range between 0 and 9999999.99 inclusive'),
            params={'money': money},
        )


def check_rating(rating: int) -> None:
    """
    Validate that rating is within the allowed range.

    Args:
        rating (int): Rating to validate.

    Raises:
        ValidationError: If rating is out of range.
    """
    if rating < 0 or rating > 5:
        raise ValidationError(
            _('The rating should be in the range between 0 and 5 inclusive'),
            params={'rating': rating},
        )


def check_quantity(quantity: int) -> None:
    """
    Validate that quantity is non-negative.

    Args:
        quantity (int): Quantity to validate.

    Raises:
        ValidationError: If quantity is negative.
    """
    if quantity < 0:
        raise ValidationError(
            _('The quantity should be greater than or equal to 0'),
            params={'quantity': quantity},
        )


class UUIDMixin(models.Model):
    """UUID Mixin."""

    id = models.UUIDField(
        primary_key=True,
        blank=True,
        editable=False,
        default=uuid4,
    )

    class Meta:
        """Meta class for UUID Mixin."""

        abstract = True


class CreatedDatetimeMixin(models.Model):
    """CreatedDatetime Mixin."""

    created_datetime = models.DateTimeField(
        _('created_datetime'),
        null=True,
        blank=True,
        default=get_current_datetime,
        validators=[check_created_datetime],
    )

    class Meta:
        """Meta class for CreatedDatetime Mixin."""

        abstract = True


class ModifiedDatetimeMixin(models.Model):
    """ModifiedDatetime Mixin."""

    modified_datetime = models.DateTimeField(
        _('modified_datetime'),
        null=True,
        blank=True,
        default=get_current_datetime,
        validators=[
            check_modified_datetime,
        ],
    )

    class Meta:
        """Meta class for ModifiedDatetime Mixin."""

        abstract = True


class Category(UUIDMixin, CreatedDatetimeMixin, ModifiedDatetimeMixin):
    """Category model."""

    title = models.TextField(
        _('title'),
        null=False,
        blank=False,
        max_length=CATEGORY_TITLE_MAX_LENGTH,
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True,
        max_length=CATEGORY_DESCRIPTION_MAX_LENGTH,
    )
    image = models.TextField(null=True, blank=True, default=DEFAULT_IMAGE)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the product.

        Returns:
            str: Title of the product along with its price.
        """
        return self.title

    class Meta:
        """Meta class for Category model."""

        db_table = '"grocery_store"."categories"'
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class ProductManager(models.Manager):
    """Product Manager."""

    def filter_by_category_title(self, category_title: str) -> None:
        """
        Filter queryset based on category title.

        Args:
            category_title (str): Title of the category to filter by.

        Returns:
            QuerySet: Filtered queryset containing instances that match the category title.
        """
        return self.get_queryset().filter(categories__title=category_title)

    def create(self, **kwargs: Any) -> Any:
        """
        Create a new instance with additional validation on provided fields.

        Args:
            **kwargs: Keyword arguments containing data for the new instance.

        Returns:
            Any: The newly created instance.
        """
        if 'price' in kwargs.keys():
            check_price(kwargs['price'])
        if 'created_datetime' in kwargs.keys():
            check_created_datetime(kwargs['created_datetime'])
        if 'check_modified_datetime' in kwargs.keys():
            check_modified_datetime(kwargs['check_modified_datetime'])
        return super().create(**kwargs)


class Product(UUIDMixin, CreatedDatetimeMixin, ModifiedDatetimeMixin):
    """Product model."""

    title = models.TextField(
        _('title'),
        null=False,
        blank=False,
        max_length=PRODUCT_TITLE_MAX_LENGTH,
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True,
        max_length=PRODUCT_DESCRIPTION_MAX_LENGTH,
    )
    price = models.DecimalField(
        _('price'),
        null=False,
        blank=False,
        max_digits=6,
        decimal_places=2,
        validators=[check_price,],
    )
    image = models.TextField(null=True, blank=True, default=DEFAULT_IMAGE)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_('category'),
        related_name='products',
    )
    promotions = models.ManyToManyField(
        'Promotion',
        through='ProductToPromotion',
        verbose_name=_('promotions'),
    )

    objects = ProductManager()

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the product.

        Returns:
            str: Title of the product along with its price.
        """
        return f'{self.title} ({self.price} {_("RUB")})'

    def save(self, *args, **kwargs):
        """
        Validate product price before saving.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            ValidationError: If the product's price is not within the allowed range.
        """
        check_price(self.price)
        super().save(*args, **kwargs)

    class Meta:
        """Meta class for Product model."""

        db_table = '"grocery_store"."products"'
        ordering = ['category', 'title', 'price']
        verbose_name = _('product')
        verbose_name_plural = _('products')


class PromotionManager(models.Manager):
    """Promotion Manager."""

    def create(self, **kwargs: Any) -> Any:
        """
        Create a new instance with additional validation on provided fields.

        Args:
            **kwargs: Keyword arguments containing data for the new instance.

        Returns:
            Any: The newly created instance.
        """
        if 'discount_amount' in kwargs.keys():
            check_discount_amount(kwargs['discount_amount'])
        if 'start_date' in kwargs.keys():
            check_start_date(kwargs['start_date'])
        if 'end_date' in kwargs.keys():
            check_end_date(kwargs['end_date'])
        if 'created_datetime' in kwargs.keys():
            check_created_datetime(kwargs['created_datetime'])
        if 'check_modified_datetime' in kwargs.keys():
            check_modified_datetime(kwargs['check_modified_datetime'])
        return super().create(**kwargs)


class Promotion(UUIDMixin, CreatedDatetimeMixin, ModifiedDatetimeMixin):
    """Promotion model."""

    title = models.TextField(
        _('title'),
        null=False,
        blank=False,
        max_length=PROMOTION_TITLE_MAX_LENGTH,
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True,
        max_length=PROMOTION_DESCRIPTION_MAX_LENGTH,
    )
    discount_amount = models.PositiveSmallIntegerField(
        _('discount amount'), null=False, blank=False, validators=[check_discount_amount,],
    )
    start_date = models.DateField(
        _('start date'),
        null=False,
        blank=False,
        validators=[check_start_date,],
        default=get_current_date,
    )
    end_date = models.DateField(
        _('end date'),
        null=False,
        blank=False,
        validators=[check_end_date,],
        default=get_current_date,
    )
    image = models.TextField(null=True, blank=True, default=DEFAULT_IMAGE)

    products = models.ManyToManyField(
        Product,
        through='ProductToPromotion',
        verbose_name=_('products'),
    )

    objects = PromotionManager()

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the product.

        Returns:
            str: Title of the product along with its price.
        """
        return _('{0} ({1}: {2}, {3}: {4} - {5})').format(
            self.title,
            _('discount amount'),
            self.discount_amount,
            _('discount time'),
            self.start_date,
            self.end_date,
        )

    def clean(self):
        """
        Validate the start and end dates of a promotion.

        Args:
            None

        Raises:
            ValidationError: If the end date is earlier than the start date.
        """
        super().clean()
        if self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError(
                    {'end_date': _(f'The {self.end_date} should be equal {self.start_date}!'), },
                )

    def save(self, *args, **kwargs):
        """
        Validate product price before saving.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            ValidationError: If the product's price is not within the allowed range.
        """
        check_discount_amount(self.discount_amount)
        check_start_date(self.start_date)
        if self.end_date:
            check_end_date(self.end_date)
        super().save(*args, **kwargs)

    class Meta:
        """Meta class for Promotion model."""

        db_table = '"grocery_store"."promotions"'
        ordering = ['discount_amount']
        verbose_name = _('promotion')
        verbose_name_plural = _('promotions')


class ProductToPromotion(UUIDMixin, CreatedDatetimeMixin):
    """ProductToPromotion relationship."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
    )
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        verbose_name=_('promotion'),
    )

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the product.

        Returns:
            str: Title of the product along with its price.
        """
        return f'{self.product} - {self.promotion}'

    class Meta:
        """Meta class for ProductToPromotion relationship."""

        db_table = '"grocery_store"."product_to_promotion"'
        unique_together = (
            ('product', 'promotion'),
        )
        verbose_name = _('Relationship product to promotion')
        verbose_name_plural = _('Relationships product to promotion')


class ReviewManager(models.Manager):
    """Review Manager."""

    def create(self, **kwargs: Any) -> Any:
        """
        Create a new instance with additional validation on provided fields.

        Args:
            **kwargs: Keyword arguments containing data for the new instance.

        Returns:
            Any: The newly created instance.
        """
        if 'rating' in kwargs.keys():
            check_rating(kwargs['rating'])
        if 'created_datetime' in kwargs.keys():
            check_created_datetime(kwargs['created_datetime'])
        if 'check_modified_datetime' in kwargs.keys():
            check_modified_datetime(kwargs['check_modified_datetime'])
        return super().create(**kwargs)


class Review(UUIDMixin, CreatedDatetimeMixin, ModifiedDatetimeMixin):
    """Review model."""

    text = models.TextField(
        _('text'),
        null=False,
        blank=False,
        max_length=REVIEW_TEXT_MAX_LENGTH,
    )
    rating = models.PositiveSmallIntegerField(
        _('rating'), null=False, blank=False, validators=[check_rating,], default=5,
    )

    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        verbose_name=_('client'),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='reviews',
    )

    objects = ReviewManager()

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the product.

        Returns:
            str: Title of the product along with its price.
        """
        return f'{self.text} ({_("rating")}: {self.rating}/5)'

    def save(self, *args, **kwargs):
        """
        Validate product price before saving.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            ValidationError: If the product's price is not within the allowed range.
        """
        check_rating(self.rating)
        super().save(*args, **kwargs)

    class Meta:
        """Meta class for Review model."""

        db_table = '"grocery_store"."reviews"'
        ordering = ['rating']
        verbose_name = _('review')
        verbose_name_plural = _('reviews')


class ClientManager(models.Manager):
    """Client Manager."""

    def create(self, **kwargs: Any) -> Any:
        """
        Create a new instance with additional validation on provided fields.

        Args:
            **kwargs: Keyword arguments containing data for the new instance.

        Returns:
            Any: The newly created instance.
        """
        if 'money' in kwargs.keys():
            check_money(kwargs['money'])
        return super().create(**kwargs)


class Client(UUIDMixin, CreatedDatetimeMixin, ModifiedDatetimeMixin):
    """Client model."""

    money = models.DecimalField(
        _('money'),
        null=False,
        blank=False,
        max_digits=9,
        decimal_places=2,
        validators=[
            check_money,
        ],
        default=0,
    )

    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    products = models.ManyToManyField(
        Product,
        through='ClientToProduct',
        verbose_name=_('products'),
    )

    objects = ClientManager()

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the product.

        Returns:
            str: Title of the product along with its price.
        """
        return f'{self.user.username} ({self.user.first_name} {self.user.last_name})'

    def save(self, *args, **kwargs):
        """
        Validate product price before saving.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            ValidationError: If the product's price is not within the allowed range.
        """
        check_money(self.money)
        super().save(*args, **kwargs)

    class Meta:
        """Meta class for Client model."""

        db_table = '"grocery_store"."clients"'
        ordering = ['user']
        verbose_name = _('client')
        verbose_name_plural = _('clients')


class ClientToProduct(UUIDMixin, CreatedDatetimeMixin):
    """ClientToProduct relationships."""

    quantity = models.PositiveSmallIntegerField(
        _('quantity'), null=False, blank=False, validators=[check_quantity,], default=1,
    )
    price = models.DecimalField(
        _('price'),
        null=False,
        blank=False,
        max_digits=6,
        decimal_places=2,
        validators=[
            check_price,
        ],
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name=_('client'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
    )

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the product.

        Returns:
            str: Title of the product along with its price.
        """
        return f'{self.client} - {self.product}'

    def save(self, *args, **kwargs):
        """
        Validate product price before saving.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            ValidationError: If the product's price is not within the allowed range.
        """
        check_quantity(self.quantity)
        super().save(*args, **kwargs)

    class Meta:
        """Meta class for ClientToProduct relationships."""

        db_table = '"grocery_store"."client_to_product"'
        unique_together = (
            ('client', 'product', 'price'),
        )
        verbose_name = _('Relationship client to product')
        verbose_name_plural = _('Relationships client to product')
