# Generated by Django 5.0.3 on 2024-06-10 02:18

import django.db.models.deletion
import grocery_store_app.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_created_datetime], verbose_name='created_datetime')),
                ('modified_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_modified_datetime], verbose_name='modified_datetime')),
                ('title', models.TextField(max_length=100, verbose_name='title')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='description')),
                ('image', models.TextField(blank=True, default='https://acropora.ru/images/yootheme/pages/features/panel03.jpg', null=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': '"grocery_store"."categories"',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_created_datetime], verbose_name='created_datetime')),
                ('modified_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_modified_datetime], verbose_name='modified_datetime')),
                ('money', models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[grocery_store_app.models.check_money], verbose_name='money')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
                'db_table': '"grocery_store"."client"',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_created_datetime], verbose_name='created_datetime')),
                ('modified_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_modified_datetime], verbose_name='modified_datetime')),
                ('title', models.TextField(max_length=200, verbose_name='title')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, validators=[grocery_store_app.models.check_price], verbose_name='price')),
                ('image', models.TextField(blank=True, default='https://acropora.ru/images/yootheme/pages/features/panel03.jpg', null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='grocery_store_app.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': '"grocery_store"."products"',
                'ordering': ['category', 'title', 'price'],
            },
        ),
        migrations.CreateModel(
            name='ClientToProduct',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_created_datetime], verbose_name='created_datetime')),
                ('quantity', models.PositiveSmallIntegerField(default=1, validators=[grocery_store_app.models.check_quantity], verbose_name='quantity')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_store_app.client', verbose_name='client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_store_app.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Relationship client to product',
                'verbose_name_plural': 'Relationships client to product',
                'db_table': '"grocery_store"."client_to_product"',
                'unique_together': {('client', 'product')},
            },
        ),
        migrations.AddField(
            model_name='client',
            name='products',
            field=models.ManyToManyField(through='grocery_store_app.ClientToProduct', to='grocery_store_app.product', verbose_name='products'),
        ),
        migrations.CreateModel(
            name='ProductToPromotion',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_created_datetime], verbose_name='created_datetime')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_store_app.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Relationship product to promotion',
                'verbose_name_plural': 'Relationships product to promotion',
                'db_table': '"grocery_store"."product_to_promotion"',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_created_datetime], verbose_name='created_datetime')),
                ('modified_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_modified_datetime], verbose_name='modified_datetime')),
                ('title', models.TextField(max_length=200, verbose_name='title')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='description')),
                ('discount_amount', models.PositiveSmallIntegerField(validators=[grocery_store_app.models.check_discount_amount], verbose_name='discount amount')),
                ('start_date', models.DateField(default=grocery_store_app.models.get_current_date, validators=[grocery_store_app.models.check_start_date], verbose_name='start date')),
                ('end_date', models.DateField(default=grocery_store_app.models.get_current_date, validators=[grocery_store_app.models.check_end_date], verbose_name='end date')),
                ('image', models.TextField(blank=True, default='https://acropora.ru/images/yootheme/pages/features/panel03.jpg', null=True)),
                ('products', models.ManyToManyField(through='grocery_store_app.ProductToPromotion', to='grocery_store_app.product', verbose_name='products')),
            ],
            options={
                'verbose_name': 'promotion',
                'verbose_name_plural': 'promotions',
                'db_table': '"grocery_store"."promotions"',
                'ordering': ['discount_amount'],
            },
        ),
        migrations.AddField(
            model_name='producttopromotion',
            name='promotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_store_app.promotion', verbose_name='promotion'),
        ),
        migrations.AddField(
            model_name='product',
            name='promotions',
            field=models.ManyToManyField(through='grocery_store_app.ProductToPromotion', to='grocery_store_app.promotion', verbose_name='promotions'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_created_datetime], verbose_name='created_datetime')),
                ('modified_datetime', models.DateTimeField(blank=True, default=grocery_store_app.models.get_current_datetime, null=True, validators=[grocery_store_app.models.check_modified_datetime], verbose_name='modified_datetime')),
                ('text', models.TextField(max_length=1000, verbose_name='text')),
                ('rating', models.PositiveSmallIntegerField(default=5, validators=[grocery_store_app.models.check_rating], verbose_name='rating')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_store_app.client', verbose_name='client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_store_app.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
                'db_table': '"grocery_store"."reviews"',
                'ordering': ['rating'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='producttopromotion',
            unique_together={('product', 'promotion')},
        ),
    ]
