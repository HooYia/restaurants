# API mobile

Cette API est séparée des vues HTML : les endpoints utilisateurs sont dans
`restaurants/users/api/` et ceux du menu dans `restaurants/meal/api/`. Toutes
ses URL commencent par `/api/v1/`. Les URL existantes du site web ne sont pas
modifiées.

## Démarrer séparément le site web et l'API

Depuis le dossier `restaurants/` :

```bash
# Site web (pages HTML) : http://127.0.0.1:8000/
uv run python manage.py runserver 0.0.0.0:8000

# API seulement : http://127.0.0.1:8001/api/v1/
uv run python manage.py runserver 0.0.0.0:8001 --settings=config.settings.api
```

Le mobile appelle par exemple `http://10.0.2.2:8001/api/v1/` depuis l'émulateur
Android (remplacer par l'IP locale de l'ordinateur sur un téléphone physique).
La documentation interactive est disponible sur `/api/docs/` pour un compte
administrateur.

## Authentification

1. `POST /api/v1/auth/register/` avec `email`, `first_name`, `last_name`,
   `phone`, `password`, ou `POST /api/v1/auth/login/` avec `email`, `password`.
2. Conserver le champ `access` retourné.
3. Envoyer ce token dans tous les appels privés :
   `Authorization: Bearer VOTRE_ACCESS_TOKEN`.

## Endpoints principaux

| Méthode | URL | Usage |
| --- | --- | --- |
| GET | `/api/v1/categories/` | Catégories publiques |
| GET | `/api/v1/meals/` | Liste des plats disponibles |
| GET | `/api/v1/meals/{id}/` | Détail d'un plat et accompagnements possibles |
| GET | `/api/v1/boissons/` | Boissons disponibles |
| GET/POST | `/api/v1/addresses/` | Adresses du client connecté |
| PATCH/DELETE | `/api/v1/addresses/{id}/` | Modifier/supprimer une adresse |
| POST | `/api/v1/addresses/{id}/set_default/` | Définir l'adresse par défaut |
| GET | `/api/v1/orders/` | Historique des commandes |
| POST | `/api/v1/orders/create_order/` | Créer une commande |
| GET/POST | `/api/v1/custom-requests/` | Demandes sur mesure |
| GET/PUT | `/api/v1/testimonial/` | Avis du client |
| GET | `/api/v1/company-settings/` | Coordonnées et éléments publics du restaurant |
| POST | `/api/v1/newsletter/` | Inscription newsletter |
| GET/POST | `/api/v1/chat/` | Lire/envoyer les messages du client |

## Administration (token administrateur requis)

Un utilisateur administrateur se connecte avec le même endpoint de connexion,
mais son compte doit avoir `is_staff=True`. Il envoie ensuite son jeton d'accès
dans `Authorization: Bearer VOTRE_ACCESS_TOKEN`.

| Méthode | URL | Usage |
| --- | --- | --- |
| GET/POST/PATCH/DELETE | `/api/v1/admin/categories/` | Gérer les catégories |
| GET/POST/PATCH/DELETE | `/api/v1/admin/meals/` | Gérer les plats |
| GET/POST/PATCH/DELETE | `/api/v1/admin/accompaniments/` | Gérer les accompagnements |
| GET/POST/PATCH/DELETE | `/api/v1/admin/boissons/` | Gérer les boissons |
| GET/PATCH | `/api/v1/admin/orders/` | Consulter/changer le statut des commandes |
| GET/PATCH | `/api/v1/admin/custom-requests/` | Tarifer ou refuser les demandes sur mesure |
| GET | `/api/v1/admin/chats/` | Liste des conversations et messages non lus |
| GET | `/api/v1/admin/chats/{id}/` | Lire une conversation (marque les messages client lus) |
| POST | `/api/v1/admin/chats/{id}/messages/` | Répondre à un client |

Pour modifier ou supprimer un élément, ajouter son UUID à la fin de l'URL,
par exemple `PATCH /api/v1/admin/categories/{id}/`. Pour l'envoi d'une
image de plat ou de boisson, utiliser `multipart/form-data` avec le champ
`image`.

## Exemple : connexion

```bash
curl -X POST http://127.0.0.1:8001/api/v1/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{"email":"client@example.com","password":"mot-de-passe"}'
```

Utilisez ensuite le champ `access` retourné dans Swagger avec
`Bearer VOTRE_ACCESS_TOKEN`. Swagger présente le schéma de requête réellement
attendu par chaque endpoint et permet de l'essayer directement.
