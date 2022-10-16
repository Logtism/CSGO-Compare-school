from django.contrib import admin
from .models import SupportTicket, TicketReply


# Adding the support ticket and ticket reply model to the django admin page
admin.site.register(SupportTicket)
admin.site.register(TicketReply)
