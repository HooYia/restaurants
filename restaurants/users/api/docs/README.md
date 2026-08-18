# Documentation Swagger - Users

Ce dossier contient la documentation technique des endpoints de l'application users.

## Principes
- Les API sont indépendantes des templates.
- Les vues sont rangées dans le dossier `views/`.
- Les serializers sont rangés dans le dossier `serializers/`.
- Les routes sont gérées par `urls.py` et sont exposées sous `/api/v1/`.
- Chaque module de ce dossier est appliqué aux vues correspondantes avec
  `drf-spectacular`; les descriptions apparaissent donc dans Swagger.
- La documentation interactive est accessible sur `/api/docs/` et le schéma
  OpenAPI sur `/api/schema/`.

## Exemples d'endpoints
- `POST /api/v1/auth/register/`
- `POST /api/v1/auth/login/`
- `GET /api/v1/profile/`
- `GET /api/v1/cart/`
- `POST /api/v1/chat/`
