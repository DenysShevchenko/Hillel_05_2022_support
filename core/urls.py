from django.urls import path

from core.api import get_ticket, request_tickets

urlpatterns = [
    path("", request_tickets),
    path("<int:id_>/", get_ticket),
]
