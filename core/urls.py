from django.urls import path

# from core.api import get_ticket
# from core.api import TicketRetrieveAPI, TicketsCreateAPI, TicketsListAPI, TicketsUpdateAPI, TicketsDeleteAPI
from core.api import (
    CommentsCreateAPI,
    CommentsListAPI,
    TicketMainAPI,
    TicketMainAPI_id,
    TicketResolveAPI,
)

tickets_urls = [
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
    path("<int:id>/resolve/", TicketResolveAPI.as_view()),
]

comments_urls = [
    path("<int:ticket_id>/comments/", CommentsListAPI.as_view()),
    path("<int:ticket_id>/comments/create/", CommentsCreateAPI.as_view()),
]

urlpatterns = tickets_urls + comments_urls
