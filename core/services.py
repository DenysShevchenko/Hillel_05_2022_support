from core.models import Ticket


class TicketsCRUD:
    @staticmethod
    def change_resolved_status(instance: Ticket) -> Ticket:
        """Change Ticket object's resolved status to the opposite."""

        instance.resolved = not instance.resolved
        instance.save()

        return instance
