"""Swagger des vues regroupées historiques ``views/views.py``."""

from drf_spectacular.utils import extend_schema

legacy_views_doc = extend_schema(tags=["Menu public"], summary="Menu public (vues regroupées historiques)", description="Documentation des vues regroupées conservées pour compatibilité interne.")
