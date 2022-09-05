from django.urls import path

# from core.api import get_ticket
# from core.api import TicketRetrieveAPI, TicketsCreateAPI, TicketsListAPI, TicketsUpdateAPI, TicketsDeleteAPI
from core.api import TicketMainAPI, TicketMainAPI_id


urlpatterns = [
    # path("", request_tickets),
    # # path("<int:id_>/", get_ticket),
    # path("", TicketsListAPI.as_view()),
    # # # path("", include(router.urls)),
    # path("create/", TicketsCreateAPI.as_view()),
    # path("update/<int:pk>/", TicketsUpdateAPI.as_view()),
    # path("delete/<int:pk>/", TicketsDeleteAPI.as_view()),
    # path("<int:id>/", TicketRetrieveAPI.as_view()),
    path("<int:id>/", TicketMainAPI_id.as_view()),
    path("", TicketMainAPI.as_view()),
]
