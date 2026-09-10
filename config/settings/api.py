"""Configuration du processus API uniquement.

Elle réutilise la même base de données et les mêmes modèles que le site, mais
charge une table d'URLs sans aucune vue HTML.
"""

from .local import *  # noqa: F403

ROOT_URLCONF = "config.api_urls"

# ``local`` active Django Debug Toolbar pour les pages HTML. L'URLConf API ne
# contient volontairement pas ses routes ; on l'en retire donc seulement ici.
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != "debug_toolbar"]  # noqa: F405
MIDDLEWARE = [  # noqa: F405
    middleware
    for middleware in MIDDLEWARE  # noqa: F405
    if middleware != "debug_toolbar.middleware.DebugToolbarMiddleware"
]

# Le serveur API local est destiné aux tests du développeur mobile : Swagger
# doit donc être consultable dans le navigateur. Les endpoints privés restent
# protégés par leur token DRF.
SPECTACULAR_SETTINGS = {
    **SPECTACULAR_SETTINGS,  # noqa: F405
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
}
