from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from items.models import Category, Subcategory, Container, Item
from .forms import CreateSupportTicketForm, CreateTicketReplyForm
from .models import SupportTicket, TicketReply


def stat(request):
    return render(request, 'info/stat.html',
                  {
                      'total_items': len(Item.objects.filter(accepted=True).all()),
                      'total_submited_items': len(Item.objects.all()),
                      'total_pending_items': len(Item.objects.filter(accepted=False).all()),
                      'subcats': Subcategory.objects.all(),
                  })


def about(request):
    return render(request, 'info/about.html')


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
            print('okok')
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
    if ticket.author == request.user or request.user.has_perm('info.'):
        if request.method == 'POST':
            form = CreateTicketReplyForm(request.POST)
            data = form.save(commit=False)
            data.author = request.user
            data.ticket = ticket
            data.save()
        form = CreateTicketReplyForm()
        return render(request, 'info/view_ticket.html', {'ticket': ticket, 'form': form})
    else:
        return Http404('Page not found')
    