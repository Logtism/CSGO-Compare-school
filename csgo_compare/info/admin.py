from django.contrib import admin
from .models import SupportTicket, TicketReply


admin.site.register(SupportTicket)
admin.site.register(TicketReply)
