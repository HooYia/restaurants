"""Swagger des vues historiques ``views/meal.py``."""

from drf_spectacular.utils import extend_schema

legacy_meal_list_doc = extend_schema(tags=["Menu public"], summary="Lister les plats (vue historique)", description="Documentation de la vue de plats conservée pour compatibilité interne.")
legacy_boisson_list_doc = extend_schema(tags=["Menu public"], summary="Lister les boissons (vue historique)", description="Documentation de la vue de boissons conservée pour compatibilité interne.")
