from django.views.generic import TemplateView
from restaurants.users.cart import Cart

class CartView(TemplateView):
    template_name = "pages/panier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        return context
