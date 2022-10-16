from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from info.models import SupportTicket
from items.models import Item
from .forms import UpdateItemForm


def dashboard(request):
    if request.user.is_staff:
        return render(
            request,
            'site_admin/dashboard.html',
            {
                'pending_items': len(
                    Item.objects.filter(accepted=False).all()
                ),
                'pending_tickets': len(
                    SupportTicket.objects.filter(closed=False).all()
                ),
                'total_users': len(User.objects.all())
            }
        )
    else:
        return HttpResponseNotFound('This page does not exist')


def items(request):
    if request.user.has_perm('items.can_view_item_sub'):
        return render(
            request,
            'site_admin/items.html',
            {
                'items': Item.objects.filter(accepted=False).all(),
                'total_item_sub': len(Item.objects.all()),
                'total_accepted_sub': len(
                    Item.objects.filter(accepted=True).all()
                ),
                'total_pending_sub': len(
                    Item.objects.filter(accepted=False).all()
                )
            }
        )
    else:
        return HttpResponseNotFound('This page does not exist')


def review_item(request, id):
    if request.user.has_perm('items.can_view_item_sub'):
        item = Item.objects.get_object_or_404(id=id)
        if request.method == 'POST':
            form = UpdateItemForm(instance=item, data=request.POST)
            if form.is_valid():
                form.save()
        else:
            form = UpdateItemForm(instance=item)
        return render(
            request,
            'site_admin/review_item.html',
            {
                'item': item,
                'form': form
            }
        )
    else:
        return HttpResponseNotFound('This page does not exist')


def item_preview(request, id):
    if request.user.has_perm('items.can_view_item_sub'):
        item = Item.objects.get_object_or_404(id=id)
        return render(request, 'items/item.html', {'item': item})
    else:
        return HttpResponseNotFound('This page does not exist')


def item_accept(request, id):
    if request.user.has_perm('items.can_accept_item_sub'):
        item = Item.objects.get_object_or_404(id=id)
        item.accepted = True
        item.save()
        return redirect(reverse('admin-items'))
    else:
        return HttpResponseNotFound('This page does not exist')


def item_delete(request, id):
    if request.user.has_perm('items.can_decline_item_sub'):
        item = Item.objects.get_object_or_404(id=id)
        item.delete()
        return redirect(reverse('admin-items'))
    else:
        return HttpResponseNotFound('This page does not exist')


def support(request):
    if request.user.has_perm('info.can_view_support_ticket'):
        tickets = SupportTicket.objects.filter(closed=False).all()
        return render(
            request,
            'site_admin/support.html',
            {
                'tickets': tickets,
                'total_tickets': len(SupportTicket.objects.all()),
                'total_sloved_tickets': len(
                    SupportTicket.objects.filter(closed=True).all()
                ),
                'total_pending_tickets': len(
                    SupportTicket.objects.filter(closed=False).all()
                ),
            }
        )
    else:
        return HttpResponseNotFound('This page does not exist')
