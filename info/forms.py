from django import forms
from .models import SupportTicket, TicketReply


class CreateSupportTicketForm(forms.ModelForm):
    
    class Meta:
        model = SupportTicket
        fields = ['title', 'body']
        
        
class CreateTicketReplyForm(forms.ModelForm):
    
    class Meta:
        model = TicketReply
        fields = ['body']