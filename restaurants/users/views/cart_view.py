from django.views.generic import TemplateView

class CartView(TemplateView):
    template_name = "pages/panier.html"
