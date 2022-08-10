from django.urls import path

from core.api import get_all_tickets, get_ticket

urlpatterns = [
    path("", get_all_tickets),
    path("<int:id_>/", get_ticket),
]
