from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib import messages
from restaurants.meal.models import CustomOrderRequest
from restaurants.meal.forms import CustomOrderRequestForm

class ClientCustomRequestCreateView(LoginRequiredMixin, CreateView):
    model = CustomOrderRequest
    form_class = CustomOrderRequestForm
    template_name = "pages/dashboard/user_dashboad/custom_request_create.html"
    success_url = reverse_lazy("users:custom-request-list")

    def form_valid(self, form):
        form.instance.client = self.request.user.client_profile
        messages.success(self.request, "Votre demande sur mesure a été envoyée ! Nous vous répondrons très vite avec une proposition de prix.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'custom_requests'
        return context

class ClientCustomRequestListView(LoginRequiredMixin, ListView):
    model = CustomOrderRequest
    template_name = "pages/dashboard/user_dashboad/custom_request_list.html"
    context_object_name = "requests"

    def get_queryset(self):
        return CustomOrderRequest.objects.filter(client=self.request.user.client_profile).order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'custom_requests'
        return context
