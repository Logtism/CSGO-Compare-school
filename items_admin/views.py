from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.urls import reverse
from .forms import UpdateItemForm
from items.models import Item


def dashboard(request):
    if request.user.has_perm('items.can_view_item_sub'):
        return render(request, 'items_admin/dashboard.html', {'items': Item.objects.filter(accepted=False).all()})
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
            'items_admin/review_item.html',
            {
                'item': item,
                'form': form
            }
        )
    else:
        return HttpResponseNotFound('This page does not exist')


def item_accept(request, id):
    if request.user.has_perm('items.can_accept_item_sub'):
        item = Item.objects.get_object_or_404(id=id)
        item.accepted = True
        item.save()
        return redirect(reverse('items-admin-item', args=[id]))
    else:
        return HttpResponseNotFound('This page does not exist')
    
    
def item_delete(request, id):
    if request.user.has_perm('items.can_decline_item_sub'):
        item = Item.objects.get_object_or_404(id=id)
        item.delete()
        return redirect(reverse('items-admin-dashboard'))
    else:
        return HttpResponseNotFound('This page does not exist')