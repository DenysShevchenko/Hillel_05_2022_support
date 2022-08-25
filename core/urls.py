from django.urls import path

from core.api import request_tickets, get_ticket

urlpatterns = [
    path("", request_tickets),
    path("<int:id_>/", get_ticket),
]
