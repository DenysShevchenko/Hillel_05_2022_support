from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from core.models import Comment, Ticket
from core.serializers import CommentSerializer


class CommentsListAPI(ListAPIView):
    http_method_names = ["get"]
    serializer_class = CommentSerializer
    lookup_field = "ticket_id"
    lookup_url_kwarg = "ticket_id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ticket_id: int = self.kwargs[self.lookup_field]
        ticket = Ticket.objects.get(id=ticket_id)
        user = self.request.user

        if ticket.client != user and ticket.operator != user:
            raise ValueError("You can see comments only if you are operator or client of this ticket")

        return Comment.objects.filter(
            ticket_id=ticket_id,
        )


class CommentsCreateAPI(CreateAPIView):

    http_method_names = ["post"]
    serializer_class = CommentSerializer
    lookup_field = "ticket_id"
    lookup_url_kwarg = "ticket_id"

    def get_queryset(self):
        ticket_id: int = self.kwargs[self.lookup_field]

        # NOTE: Walrus operator usage
        if ticket_id := self.kwargs.get(self.lookup_field):
            raise ValueError("You can not comment unspecified ticket.")

        return Comment.objects.filter(ticket_id=ticket_id)
