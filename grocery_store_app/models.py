from django.conf.global_settings import AUTH_USER_MODEL
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime, date, timezone
from uuid import uuid4


CATEGORY_TITLE_MAX_LENGTH = 100
CATEGORY_DESCRIPTION_MAX_LENGTH = 1000
PRODUCT_AND_PROMOTION_TITLE_MAX_LENGTH = 200
PRODUCT_AND_PROMOTION_DESCRIPTION_MAX_LENGTH = 2000
REVIEW_TEXT_MAX_LENGTH = 1000


def get_datetime():
    return datetime.now(timezone.utc)

def check_created_datatime(created_datatime: datetime) -> None:
    if created_datatime > get_datetime():
        raise ValidationError(
            _('Created datatime is bigger than current datetime!'),
            params={'created_datatime': created_datatime}
        )

def check_modified_datatime(modified_datatime: datetime) -> None:
    if modified_datatime > get_datetime():
        raise ValidationError(
            _('Modified datatime is bigger than current datetime!'),
            params={'modified_datatime': modified_datatime}
        )
    
def check_start_date(start_date: date) -> None:
    if start_date > date.today():
        raise ValidationError(
            _('Start date is bigger than current date!'),
            params={'start_date': start_date},
        )

def check_end_date(end_date: date) -> None:
    if end_date > date.today():
        raise ValidationError(
            _('End date is bigger than current date!'),
            params={'end_date': end_date},
        )
    
def check_positive(number: int | float) -> None:
    if number < 0:
        raise ValidationError(_('Value has to be greater than zero!'))
    
def check_max_discount_amount(discount_amount: int) -> None:
    if discount_amount > 100:
        raise ValidationError(_('Discount amount has to be less than one hundred!'))
    
def check_max_rating(rating: int) -> None:
    if rating > 5:
        raise ValidationError(_('Rating has to be less than five!'))


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        abstract = True


class CreatedDatatimeMixin(models.Model):
    created_datatime = models.DateTimeField(
        _('created_datatime'),
        null=True, blank=True,
        default=get_datetime, 
        validators=[
            check_created_datatime,
        ]
    )

    class Meta:
        abstract = True


class ModifiedDatatimeMixin(models.Model):
    modified_datatime = models.DateTimeField(
        _('modified_datatime'),
        null=True, blank=True,
        default=get_datetime, 
        validators=[
            check_modified_datatime,
        ]
    )

    class Meta:
        abstract = True


class Category(UUIDMixin, CreatedDatatimeMixin, ModifiedDatatimeMixin):
    title = models.TextField(_('title'), null=False, blank=False, max_length=CATEGORY_TITLE_MAX_LENGTH)
    description = models.TextField(_('description'), null=True, blank=True, max_length=CATEGORY_DESCRIPTION_MAX_LENGTH)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = '"grocery_store"."categories"'
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class CategoryToCategory(UUIDMixin, CreatedDatatimeMixin):
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('parent_category'), related_name='child_categories')
    child_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('child_category'), related_name='parent_categories')

    def __str__(self) -> str:
        return f'{self.parent_category} - {self.child_category}'

    class Meta:
        db_table = '"grocery_store"."category_to_category"'
        unique_together = (
            ('parent_category', 'child_category'),
        )
        verbose_name = _('Relationship category to category')
        verbose_name_plural = _('Relationships category to category')


class Product(UUIDMixin, CreatedDatatimeMixin, ModifiedDatatimeMixin):
    title = models.TextField(_('title'), null=False, blank=False, max_length=PRODUCT_AND_PROMOTION_TITLE_MAX_LENGTH)
    description = models.TextField(_('description'), null=True, blank=True, max_length=PRODUCT_AND_PROMOTION_DESCRIPTION_MAX_LENGTH)
    price = models.DecimalField(_('price'), null=False, blank=False, max_digits=7, decimal_places=2, validators=[check_positive], default=0)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('category'))
    promotions = models.ManyToManyField('Promotion', through='ProductToPromotion', verbose_name=_('promotions'))

    def __str__(self) -> str:
        return f'{self.title} ({self.price} {_("rubles")})'

    class Meta:
        db_table = '"grocery_store"."products"'
        ordering = ['category', 'title', 'price']
        verbose_name = _('product')
        verbose_name_plural = _('products')


class Promotion(UUIDMixin, CreatedDatatimeMixin, ModifiedDatatimeMixin):
    title = models.TextField(_('title'), null=False, blank=False, max_length=PRODUCT_AND_PROMOTION_TITLE_MAX_LENGTH)
    description = models.TextField(_('description'), null=True, blank=True, max_length=PRODUCT_AND_PROMOTION_DESCRIPTION_MAX_LENGTH)
    discount_amount = models.PositiveSmallIntegerField(_('discount amount'), null=False, blank=False, validators=[check_max_discount_amount], default=0)
    start_date = models.DateField(_('start date'), null=False, blank=False, validators=[check_start_date])
    end_date = models.DateField(_('end date'), null=True, blank=True, validators=[check_end_date])

    products = models.ManyToManyField(Product, through='ProductToPromotion', verbose_name=_('products'))

    def clean(self):
        super().clean()
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError({
                'end_date': _(f'The {self.end_date} should be greater than or equal to the {self.start_date}'),
            })
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        db_table = '"grocery_store"."promotions"'
        ordering = ['discount_amount']
        verbose_name = _('promotion')
        verbose_name_plural = _('promotions')


class Review(UUIDMixin, CreatedDatatimeMixin, ModifiedDatatimeMixin):
    text = models.TextField(_('text'), null=False, blank=False, max_length=REVIEW_TEXT_MAX_LENGTH)
    rating = models.PositiveSmallIntegerField(_('rating'), null=True, blank=True, validators=[check_max_rating], default=5)

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))

    def __str__(self) -> str:
        return f'{self.text}; {_("rating")} {self.rating}/5'
    
    class Meta:
        db_table = '"grocery_store"."reviews"'
        ordering = ['rating']
        verbose_name = _('review')
        verbose_name_plural = _('reviews')


class ProductToPromotion(UUIDMixin, CreatedDatatimeMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, verbose_name=_('promotion'))

    def __str__(self) -> str:
        return f'{self.product} - {self.promotion}'

    class Meta:
        db_table = '"grocery_store"."product_to_promotion"'
        unique_together = (
            ('product', 'promotion'),
        )
        verbose_name = _('Relationship product to promotion')
        verbose_name_plural = _('Relationships product to promotion')


class Client(UUIDMixin, CreatedDatatimeMixin, ModifiedDatatimeMixin):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    money = models.DecimalField(_('money'), null=True, blank=True, decimal_places=2, max_digits=10, validators=[check_positive], default=0)

    def __str__(self) -> str:
        return f'{self.user.username} ({self.user.first_name} {self.user.last_name})'
    
    class Meta:
        db_table = '"grocery_store"."client"'
        verbose_name = _('client')
        verbose_name_plural = _('clients')