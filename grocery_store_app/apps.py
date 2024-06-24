"""Apps module."""

from django.apps import AppConfig


class GroceryStoreAppConfig(AppConfig):
    """Set up AppConfig for grocery_store_app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'grocery_store_app'
