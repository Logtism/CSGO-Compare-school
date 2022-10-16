from django.db import models
from django.contrib.auth.models import User


class SupportTicket(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=1000)
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('can_view_support_ticket', 'Can view support tickets.'),
            ('can_reply_support_ticket', 'Can reply to support tickets.'),
            ('can_close_support_ticket', 'Can close support tickets.')
        )

    def __str__(self):
        return f'{self.title}'


class TicketReply(models.Model):
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ticket.title}:{self.author.username}'
