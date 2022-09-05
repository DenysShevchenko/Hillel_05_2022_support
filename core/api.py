from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from core.models import Ticket
from core.serializers import TicketLightSerializer, TicketSerializer


class TicketsListAPI(ListAPIView):
    serializer_class = TicketLightSerializer
    queryset = Ticket.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_anonymous is True:
            return Ticket.objects.all()
        elif self.request.user.role_id != 1:
            return Ticket.objects.filter(client=self.request.user)
        else:
            return Ticket.objects.filter(operator=self.request.user) | Ticket.objects.filter(operator=None)


class TicketsCreateAPI(CreateAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]


class TicketRetrieveAPI(RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        if self.request.user.is_anonymous is True:
            return Ticket.objects.all()
        elif self.request.user.role_id != 1:
            return Ticket.objects.filter(client=self.request.user)
        else:
            return Ticket.objects.all()


class TicketsUpdateAPI(UpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TicketLightSerializer
    queryset = Ticket.objects.all()

    def get_queryset(self):
        breakpoint()
        # if self.request.user.is_anonymous is True:
        return Ticket.objects.all()


class TicketsDeleteAPI(DestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TicketLightSerializer
    queryset = Ticket.objects.all()


class TicketMainAPI_id(TicketRetrieveAPI, TicketsUpdateAPI, TicketsDeleteAPI, TicketsCreateAPI, TicketsListAPI):

    queryset = Ticket.objects.all()


class TicketMainAPI(TicketsCreateAPI, TicketsListAPI):

    queryset = Ticket.objects.all()
