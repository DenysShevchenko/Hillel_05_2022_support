from django.http import JsonResponse


class TicketsService:
    def get_all_tickets(self):
        return {}


def get_all_tickets(request):
    tickets_service = TicketsService()
    data = tickets_service.get_all_tickets()
    return JsonResponse(data)
