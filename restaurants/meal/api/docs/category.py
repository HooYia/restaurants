"""Swagger de la vue historique ``views/category.py``."""

from drf_spectacular.utils import extend_schema

legacy_category_list_doc = extend_schema(tags=["Menu public"], summary="Lister les catégories (vue historique)", description="Documentation de la vue de catégories conservée pour compatibilité interne.")
