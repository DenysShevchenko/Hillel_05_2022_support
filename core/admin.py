from django.contrib import admin

from .models import Comment, Ticket

# @admin.site.register(User)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "operator", "client", "theme"]
    list_filter = ["client", "operator"]
    # pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "ticket"]
