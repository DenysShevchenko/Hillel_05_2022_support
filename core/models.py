from django.conf import settings
from django.db import models

from shared.django.models import TimeStampMixin


class Ticket(TimeStampMixin):
    theme = models.CharField(max_length=255)
    description = models.TextField()
    resolved = models.BooleanField(default=False)

    # NOTE: Only users with role=USER could be assigned as a client
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_tickets",
    )

    # NOTE: Only users with role=ADMIN could be assigned as a client
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="operator_tickets",
    )

    def __str__(self):
        return f"{self.operator} | {self.theme}"


class Comment(TimeStampMixin):
    text = models.TextField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments",
    )
    ticket = models.ForeignKey(
        "Ticket",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    prev_comment = models.OneToOneField(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next",
    )

    def __str__(self):
        return str(self.ticket)


# Ticket.objects.get(id=4)
# Ticket.objects.all()
# Ticket.objects.filter(client=User(...))
# Ticket.objects.first()
# Ticket.objects.last()
# Ticket.objects.create(...)
# Ticket.objects.update(...)
# Ticket.objects.delete(id=...)

# ticket_445 = Ticket.objects.get(id=445)
# ticket_445.client
# ticket_445.operator

# admin = User.objects.get(email='admin@admin.com')
# tickets = Ticket.ojects.filter(operator=admin)
# admin.operator_ticket.all()
