from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from info.models import SupportTicket
from items.models import Item
from .forms import UpdateItemForm


def dashboard(request):
    '''
    The admin dashboard display some info about the site.
    '''
    # Making sure that the user is staff
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
        # If the user is not staff return a 404 error
        # returns a 404 instead of a 403 because do not want to let
        # users who are not admins know the admin page route
        return HttpResponseNotFound('This page does not exist')


def items(request):
    '''
    Display a list of all the unreviewed items.
    '''
    # Check that the user should be able to access the page
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
        # If the user does not have permission to access the page
        # return a 404 error
        # returns a 404 instead of a 403 because do not want to let
        # users who are not admins know the admin page route
        return HttpResponseNotFound('This page does not exist')


def review_item(request, id):
    '''
    Give more detailed info about an unreviewed item.
    '''
    # Check that the user should be able to access the page
    if request.user.has_perm('items.can_view_item_sub'):
        # Get the item or return a 404 error
        item = Item.objects.get_object_or_404(id=id)
        if request.method == 'POST':
            # If the request is a post initialize the form with
            # the instance of the item and the post data
            form = UpdateItemForm(instance=item, data=request.POST)
            if form.is_valid():
                # If the form is valid save the changes
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
        # If the user does not have permission to access the page
        # return a 404 error
        # returns a 404 instead of a 403 because do not want to let
        # users who are not admins know the admin page route
        return HttpResponseNotFound('This page does not exist')


def item_preview(request, id):
    '''
    A preview of what the item page will look like.
    '''
    # Check that the user should be able to access the page
    if request.user.has_perm('items.can_view_item_sub'):
        # Get the item or return a 404 error
        item = Item.objects.get_object_or_404(id=id)
        return render(request, 'items/item.html', {'item': item})
    else:
        # If the user does not have permission to access the page
        # return a 404 error
        # returns a 404 instead of a 403 because do not want to let
        # users who are not admins know the admin page route
        return HttpResponseNotFound('This page does not exist')


def item_accept(request, id):
    '''
    Accept an item so it will be displayed on the site.
    '''
    # Check that the user should be able to access the page
    if request.user.has_perm('items.can_accept_item_sub'):
        # Get the item or return a 404 error
        item = Item.objects.get_object_or_404(id=id)
        # Update it to be accepted
        item.accepted = True
        item.save()
        # Send the user back to the list of unreviewed items
        return redirect(reverse('admin-items'))
    else:
        # If the user does not have permission to access the page
        # return a 404 error
        # returns a 404 instead of a 403 because do not want to let
        # users who are not admins know the admin page route
        return HttpResponseNotFound('This page does not exist')


def item_delete(request, id):
    '''
    Decline an item so it will not be shown on the site and be deleted.
    '''
    # Check that the user should be able to access the page
    if request.user.has_perm('items.can_decline_item_sub'):
        # Get the item or return a 404 error
        item = Item.objects.get_object_or_404(id=id)
        # Delete the item
        item.delete()
        # Send the user back to the list of unreviewed items
        return redirect(reverse('admin-items'))
    else:
        # If the user does not have permission to access the page
        # return a 404 error
        # returns a 404 instead of a 403 because do not want to let
        # users who are not admins know the admin page route
        return HttpResponseNotFound('This page does not exist')


def support(request):
    '''
    Display a list of open support tickets.
    '''
    # Check that the user should be able to access the page
    if request.user.has_perm('info.can_view_support_ticket'):
        # Get the list of all the open tickets
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
        # If the user does not have permission to access the page
        # return a 404 error
        # returns a 404 instead of a 403 because do not want to let
        # users who are not admins know the admin page route
        return HttpResponseNotFound('This page does not exist')
