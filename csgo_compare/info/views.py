from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from items.models import Subcategory, Item
from .forms import CreateSupportTicketForm, CreateTicketReplyForm
from .models import SupportTicket


def stat(request):
    '''
    Statistics page showing info about the numbers of items for each weapon.
    '''
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
    '''
    About page exampling the purpose of the site.
    '''
    return render(request, 'info/about.html')


def faq(request):
    '''
    FAQ page answering common questions.
    '''
    return render(request, 'info/faq.html')


@login_required
def create_ticket(request):
    '''
    Create ticket page with a form to create a support ticket.
    '''
    if request.method == 'POST':
        # If request is a post initialize form with post data
        form = CreateSupportTicketForm(request.POST)
        if form.is_valid():
            # If the form is valid add an author to the ticket
            # The author just the user that is viewing the page
            # and saving the ticket to the database
            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.save()
            # redicrecting the user to the home page.
            return redirect('base-home')
    else:
        form = CreateSupportTicketForm()
    return render(request, 'info/create_ticket.html', {'form': form})


@login_required
def tickets_list(request):
    '''
    Display a list of the users support tickets
    '''
    # Getting a list of the user support tickets.
    tickets = SupportTicket.objects.filter(author=request.user).all()
    return render(request, 'info/tickets_list.html', {'tickets': tickets})


@login_required
def view_ticket(request, id):
    '''
    View a support ticket in more detail.
    '''
    # Get the ticket from database or give a 404 if it does not exist
    ticket = SupportTicket.objects.get_object_or_404(id=id)
    # Checking that the user is either the author or
    # has permission to view support tickets
    if (
        ticket.author == request.user or
        request.user.has_perm('info.can_view_support_ticket')
    ):
        if request.method == 'POST':
            if (
                ticket.author == request.user or
                request.user.has_perm('info.can_reply_support_ticket')
            ):
                # The request is a post and is made by the ticket author
                # or has permission to reply to support tickets
                form = CreateTicketReplyForm(request.POST)
                if form.is_valid():
                    # If the form is valid add a author and the ticket its
                    # on to the reply and save it to the database
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
        # If the user trying to access the page is not the author or
        # has permission to view tickets return a 404
        return HttpResponseNotFound('Page not found')


@login_required
def close_ticket(request, id):
    # Get the ticket from database or give a 404 if it does not exist
    ticket = SupportTicket.objects.get_object_or_404(id=id)
    # Checking that the user is either the author or
    # has permission to close support tickets
    if (
        ticket.author == request.user or
        request.user.has_perm('info.can_close_support_ticket')
    ):
        # Deleting the support ticket
        SupportTicket.objects.filter(id=ticket.id).delete()
        if ticket.author == request.user:
            # If the user is the author send them to the home page
            return redirect(reverse('base-home'))
        else:
            # If the user is an admin send them to the admin support admin
            return redirect(reverse('admin-support'))
    else:
        # If the user trying to access the page is not the author or
        # has permission to close tickets return a 404
        return HttpResponseNotFound('Page not found')
