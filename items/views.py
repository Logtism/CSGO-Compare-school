from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .models import Subcategory, Collection, Item
from .forms import AddItemForm
import requests


def subcat(request, id):
    subcat_ = Subcategory.objects.get_object_or_404(id=id)
    return render(request, 'items/subcat.html', {'subcat': subcat_})


def collection(request, id):
    collection_ = Collection.objects.get_object_or_404(id=id)
    return render(request, 'items/collection.html', {'collection': collection_})


def item(request, id):
    item = Item.objects.get_object_or_404(id=id, accepted=True)
    
    skinport = {'fn': 0, 'mw': 0, 'ft': 0, 'ww': 0, 'bs': 0}
    skinport_wears = {2: 'fn', 4: 'mw', 3: 'ft', 5: 'ww', 1: 'bs'}
    
    for wear in skinport_wears:
        r = requests.get(
            f"https://skinport.com/api/browse/730?{item.skinport_id}&sort=price&order=asc&exterior={wear}",
            headers={
                'Referer': 'https://skinport.com/api/browse/730',
                'Cookie': 'i18n=en; _csrf=-OYf7uAQmPZwniD-123456-p'
            }
        )
        if len(r.json()['items']) > 0:
            skinport[skinport_wears[wear]] = r.json()['items'][0]['salePrice'] / 100
    
    return render(request, 'items/item.html', {'item': item, 'skinport': skinport})


@login_required
def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.added_by = Profile.objects.get(user=request.user)
            data.save()
    else:
        form = AddItemForm()
    
    return render(request, 'items/add_item.html', {'form': form})