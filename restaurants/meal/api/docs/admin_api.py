"""Swagger de toutes les fonctionnalités de ``views/admin_api.py``."""

from .admin import (
    admin_accompaniment_create_doc, admin_accompaniment_delete_doc, admin_accompaniment_detail_doc,
    admin_accompaniment_list_doc, admin_accompaniment_update_doc,
    admin_boisson_create_doc, admin_boisson_delete_doc, admin_boisson_detail_doc,
    admin_boisson_list_doc, admin_boisson_update_doc,
    admin_category_create_doc, admin_category_delete_doc, admin_category_detail_doc,
    admin_category_list_doc, admin_category_update_doc,
    admin_custom_request_detail_doc, admin_custom_request_list_doc, admin_custom_request_update_doc,
    admin_meal_create_doc, admin_meal_delete_doc, admin_meal_detail_doc,
    admin_meal_list_doc, admin_meal_update_doc,
    admin_order_detail_doc, admin_order_list_doc, admin_order_update_doc,
)

__all__ = [name for name in globals() if name.startswith("admin_")]
