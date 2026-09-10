# Documentation Swagger - Meal

Ce dossier contient la documentation technique des endpoints de l'application meal.

## Principes
- Les APIs sont indépendantes des templates.
- Les vues sont rangées dans le dossier `views/`.
- Les serializers sont rangés dans le dossier `serializers/`.
- Les routes sont exposées sous `/api/v1/`.
- Les descriptions de `menu.py` et `admin.py` sont directement liées aux vues
  et apparaissent dans Swagger.
- Swagger est disponible à la racine du serveur API et sous `/api/docs/`.

## Exemples d'endpoints
- `GET /api/v1/categories/`
- `GET /api/v1/boissons/`
- `GET /api/v1/meals/`
- `GET /api/v1/admin/categories/`
