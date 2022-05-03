from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .models import Subcategory, Item
from .forms import AddItemForm


def items(request, id):
    subcat = Subcategory.objects.get_object_or_404(id=id)
    return render(request, 'items/items.html', {'subcat': subcat})


def item(request, id):
    item = Item.objects.get_object_or_404(id=id, accepted=True)
    return render(request, 'items/item.html', {'item': item})


@login_required
def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.added_by = Profile.objects.get(user=request.user)
            data.save()
    else:
        form = AddItemForm()
    
    return render(request, 'items/add_item.html', {'form': form})