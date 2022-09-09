from django.db.models import Q
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from authentication.models import DEFAULT_ROLES
from core.models import Ticket

# from core.permissions import OperatorOnly
from core.serializers import (
    TicketAssignSerializer,
    TicketLightSerializer,
    TicketSerializer,
)

# from rest_framework.response import Response
# from rest_framework import status

# from django.core.exceptions import ValidationError


class TicketsListAPI(ListAPIView):
    serializer_class = TicketLightSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        empty = self.request.GET.get("empty")
        empty_zn = False

        if empty is not None:
            if user.role.id != DEFAULT_ROLES["admin"]:
                raise ValueError("Only Admin can use empty")
            elif empty == "true":
                empty_zn = True
            elif empty == "false":
                empty_zn = False
            else:
                raise ValueError("Bad format empty")
        if user.role.id == DEFAULT_ROLES["admin"]:
            if empty_zn is True:
                return Ticket.objects.filter(operator=None)
            else:
                return Ticket.objects.filter(Q(operator=None) | Q(operator=user))

        return Ticket.objects.filter(client=user)


class TicketsCreateAPI(CreateAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role.id == DEFAULT_ROLES["admin"]:
            return Ticket.objects.filter(Q(operator=None) | Q(operator=user))

        return Ticket.objects.filter(client=user)


class TicketRetrieveAPI(RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role.id == DEFAULT_ROLES["user"]:
            return Ticket.objects.filter(client=user)
        return Ticket.objects.filter(operator=user)


class TicketsUpdateAPI(UpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TicketLightSerializer
    queryset = Ticket.objects.all()
    # permission_classes = [OperatorOnly]
    # lookup_field = "id"
    # lookup_url_kwarg = "id"

    def get_queryset(self):
        if self.request.method == "PATCH":
            return Ticket.objects.filter(operator=None)
        return Ticket.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return TicketAssignSerializer
        return TicketLightSerializer


class TicketsDeleteAPI(DestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TicketLightSerializer
    queryset = Ticket.objects.all()


# class TicketAssignAPI(UpdateAPIView):
#     http_method_names = ["patch"]
#     serializer_class = TicketAssignSerializer
#     permission_classes = [OperatorOnly]
#     lookup_field = "id"
#     lookup_url_kwarg = "id"

#     def get_queryset(self):
#         return Ticket.objects.filter(operator=None)


class TicketMainAPI_id(TicketsUpdateAPI, TicketRetrieveAPI, TicketsDeleteAPI):

    queryset = Ticket.objects.all()


class TicketMainAPI(TicketsListAPI, TicketsCreateAPI):

    queryset = Ticket.objects.all()
