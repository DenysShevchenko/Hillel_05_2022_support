from django.contrib.auth import get_user_model
from rest_framework import serializers

from authentication.models import Role
from core.models import Ticket

User = get_user_model()


def user_as_dict(user):
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
    operator = UserSerializer(read_only=True)
    client = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketLightSerializer(serializers.ModelSerializer):
    operator = UserSerializer(read_only=True)
    client = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "theme", "description", "resolved", "operator", "client"]
