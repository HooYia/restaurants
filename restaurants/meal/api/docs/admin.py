"""Documentation Swagger de l'administration du menu."""

from drf_spectacular.utils import OpenApiResponse, extend_schema


ADMIN_MENU_TAG = "Administration du menu"


def crud_doc(summary, description):
    return extend_schema(
        tags=[ADMIN_MENU_TAG],
        summary=summary,
        description=description + " Cette opération exige un compte administrateur.",
        responses={401: OpenApiResponse(description="Authentification requise."), 403: OpenApiResponse(description="Accès réservé aux administrateurs.")},
    )


admin_category_list_doc = crud_doc("Lister les catégories", "Retourne toutes les catégories, actives ou non.")
admin_category_create_doc = crud_doc("Créer une catégorie", "Crée une catégorie de menu.")
admin_category_detail_doc = crud_doc("Consulter une catégorie", "Retourne une catégorie.")
admin_category_update_doc = crud_doc("Modifier une catégorie", "Met à jour une catégorie.")
admin_category_delete_doc = crud_doc("Supprimer une catégorie", "Supprime une catégorie.")

admin_meal_list_doc = crud_doc("Lister les plats", "Retourne tous les plats, y compris ceux indisponibles.")
admin_meal_create_doc = crud_doc("Créer un plat", "Crée un plat et permet d'associer sa catégorie et ses accompagnements.")
admin_meal_detail_doc = crud_doc("Consulter un plat", "Retourne un plat administrable.")
admin_meal_update_doc = crud_doc("Modifier un plat", "Met à jour un plat, son image, sa disponibilité ou ses accompagnements.")
admin_meal_delete_doc = crud_doc("Supprimer un plat", "Supprime un plat.")

admin_accompaniment_list_doc = crud_doc("Lister les accompagnements", "Retourne tous les accompagnements.")
admin_accompaniment_create_doc = crud_doc("Créer un accompagnement", "Crée un accompagnement.")
admin_accompaniment_detail_doc = crud_doc("Consulter un accompagnement", "Retourne un accompagnement.")
admin_accompaniment_update_doc = crud_doc("Modifier un accompagnement", "Met à jour un accompagnement.")
admin_accompaniment_delete_doc = crud_doc("Supprimer un accompagnement", "Supprime un accompagnement.")

admin_boisson_list_doc = crud_doc("Lister les boissons", "Retourne toutes les boissons, y compris celles indisponibles.")
admin_boisson_create_doc = crud_doc("Créer une boisson", "Crée une boisson; utilisez multipart/form-data pour une image.")
admin_boisson_detail_doc = crud_doc("Consulter une boisson", "Retourne une boisson.")
admin_boisson_update_doc = crud_doc("Modifier une boisson", "Met à jour une boisson, son image ou sa disponibilité.")
admin_boisson_delete_doc = crud_doc("Supprimer une boisson", "Supprime une boisson.")

admin_order_list_doc = crud_doc("Lister les commandes", "Retourne les commandes reçues, de la plus récente à la plus ancienne.")
admin_order_detail_doc = crud_doc("Consulter une commande", "Retourne une commande avec son client.")
admin_order_update_doc = crud_doc("Mettre à jour le statut d'une commande", "Seul le statut est modifiable; une commande annulée ne peut plus être modifiée.")

admin_custom_request_list_doc = crud_doc("Lister les demandes sur mesure", "Retourne les demandes de plats sur mesure.")
admin_custom_request_detail_doc = crud_doc("Consulter une demande sur mesure", "Retourne une demande sur mesure.")
admin_custom_request_update_doc = crud_doc("Traiter une demande sur mesure", "Permet notamment de proposer un prix ou de refuser une demande. La première proposition de prix crée un plat lié.")
