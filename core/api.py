from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.models import Role
from core.models import Ticket

User = get_user_model()


def user_as_dict(user: User):
    return {
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "first_name": user.phone,
        "last_name": user.phone,
        "age": user.phone,
    }


def ticket_as_dict(ticket: Ticket):
    return {
        "id": ticket.id,  # type: ignore
        "theme": ticket.theme,
        "description": ticket.description,
        "operator": user_as_dict(ticket.operator),
        "resolved": ticket.resolved,
        "created_at": ticket.created_at,
        "updated_at": ticket.updated_at,
    }


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = ["id", "role", "email", "username", "first_name", "last_name", "age", "phone"]


class TicketSerializer(serializers.ModelSerializer):
    operator = UserSerializer()
    client = UserSerializer()

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketLightSerializer(serializers.ModelSerializer):
    operator = UserSerializer()
    client = UserSerializer()

    class Meta:
        model = Ticket
        fields = ["id", "operator", "client", "theme", "description", "resolved"]


@api_view(["GET"])
def get_all_tickets(request):
    tickets = Ticket.objects.all()
    data = TicketLightSerializer(tickets, many=True).data
    return Response(data=data)


@api_view(["GET"])
def get_ticket(request, id_: int):
    tickets = Ticket.objects.get(id=id_)
    data = TicketSerializer(tickets).data
    print('1')
    return Response(data=data)
