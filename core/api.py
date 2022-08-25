from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Ticket
from core.serializers import TicketLightSerializer, TicketSerializer


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([AllowAny])
def request_tickets(request):
    request_method = request.method

    if request_method != "GET" and request.user.is_anonymous is True:
        return Response(status=status.HTTP_403_FORBIDDEN)

    func_dict = get_func_dict()
    method_func = func_dict.get(request_method)

    return method_func(request)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_ticket(request, id_: int):
    tickets = Ticket.objects.get(id=id_)
    data = TicketSerializer(tickets).data
    return Response(data=data)


def get_func_dict():

    func_list = {
        "GET": method_GET_tickets,
        "POST": method_POST_tickets,
        "PUT": method_PUT_tickets,
        "DELETE": method_DELETE_tickets,
    }

    return func_list


def method_GET_tickets(request):

    tickets = Ticket.objects.all()
    data = TicketLightSerializer(tickets, many=True).data
    return Response(data=data)


def method_DELETE_tickets(request):

    ticket = find_ticket(id_=request.data["id"])
    if ticket is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    ticket.delete()
    return Response(status=status.HTTP_200_OK)


def method_PUT_tickets(request):
    ticket = find_ticket(id_=request.data["id"])
    if ticket is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = TicketLightSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.update(ticket, validated_data=serializer.validated_data)
    results = TicketSerializer(ticket).data
    return Response(data=results, status=status.HTTP_200_OK)


def method_POST_tickets(request):
    serializer = TicketSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    instance = serializer.create(serializer.validated_data)
    results = TicketSerializer(instance).data

    return Response(data=results, status=status.HTTP_201_CREATED)


def find_ticket(id_):
    try:
        ticket = Ticket.objects.get(id=id_)
    except Ticket.DoesNotExist:
        ticket = None

    return ticket
