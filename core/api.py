from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Ticket
from core.serializers import TicketLightSerializer, TicketSerializer


@api_view(["GET", "POST", "PUT", "DELETE"])
def get_post_tickets(request):
    if request.method == "GET":
        tickets = Ticket.objects.all()
        data = TicketLightSerializer(tickets, many=True).data
        return Response(data=data)
    elif request.method == "DELETE":

        ticket = find_ticket(id_=request.data["id"])
        if ticket is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ticket.delete()
        return Response(status=status.HTTP_200_OK)
    elif request.method == "PUT":
        ticket = find_ticket(id_=request.data["id"])
        if ticket is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = TicketLightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        breakpoint()
        serializer.update(ticket, validated_data=serializer.validated_data)
        results = TicketSerializer(ticket).data
        return Response(data=results, status=status.HTTP_200_OK)

    serializer = TicketSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    instance = serializer.create(serializer.validated_data)
    results = TicketSerializer(instance).data

    return Response(data=results, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_ticket(request, id_: int):
    tickets = Ticket.objects.get(id=id_)
    data = TicketSerializer(tickets).data
    return Response(data=data)


def find_ticket(id_):
    try:
        ticket = Ticket.objects.get(id=id_)
    except Exception as err:
        print(err)
        ticket = None

    return ticket
