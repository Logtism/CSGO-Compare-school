from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from items.models import Subcategory, Item
from .forms import CreateSupportTicketForm, CreateTicketReplyForm
from .models import SupportTicket


def stat(request):
    return render(
        request,
        'info/stat.html',
        {
            'total_items': len(Item.objects.filter(accepted=True).all()),
            'total_submited_items': len(Item.objects.all()),
            'total_pending_items': len(
                Item.objects.filter(accepted=False).all()
            ),
            'subcats': Subcategory.objects.all(),
        }
    )


def about(request):
    return render(request, 'info/about.html')


def faq(request):
    return render(request, 'info/faq.html')


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = CreateSupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.save()
            return redirect('base-home')
    else:
        form = CreateSupportTicketForm()

    return render(request, 'info/create_ticket.html', {'form': form})


@login_required
def tickets_list(request):
    tickets = SupportTicket.objects.filter(author=request.user).all()
    return render(request, 'info/tickets_list.html', {'tickets': tickets})


@login_required
def view_ticket(request, id):
    ticket = SupportTicket.objects.get_object_or_404(id=id)
    if (
        ticket.author == request.user or
        request.user.has_perm('info.can_view_support_ticket')
    ):
        if request.method == 'POST':
            if (
                ticket.author == request.user or
                request.user.has_perm('info.can_reply_support_ticket')
            ):
                form = CreateTicketReplyForm(request.POST)
                data = form.save(commit=False)
                data.author = request.user
                data.ticket = ticket
                data.save()
        form = CreateTicketReplyForm()
        return render(
            request,
            'info/view_ticket.html',
            {
                'ticket': ticket,
                'form': form
            }
        )
    else:
        return HttpResponseNotFound('Page not found')


@login_required
def close_ticket(request, id):
    ticket = SupportTicket.objects.get_object_or_404(id=id)
    if (
        ticket.author == request.user or
        request.user.has_perm('info.can_close_support_ticket')
    ):
        SupportTicket.objects.filter(id=ticket.id).delete()
        if ticket.author == request.user:
            return redirect(reverse('base-home'))
        else:
            return redirect(reverse('admin-support'))
    else:
        return HttpResponseNotFound('Page not found')
