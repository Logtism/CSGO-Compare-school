from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .models import Subcategory, Collection, Pattern, Item
from .forms import AddItemForm


def subcat(request, id):
    subcat_ = Subcategory.objects.get_object_or_404(id=id)
    return render(
        request,
        'items/items_list.html', 
        {
            'items': subcat_.items.all(),
            'top_bar': True,
            'collection_name': f'{subcat_.name} Skins'
        }
    )


def collection(request, id):
    collection_ = Collection.objects.get_object_or_404(id=id)
    return render(
        request,
        'items/items_list.html', 
        {
            'items': collection_.collection_items.all(),
            'top_bar': True,
            'collection_name': f'{collection_.name}'
        }
    )


def pattern(request, id):
    pattern = Pattern.objects.get_object_or_404(id=id)
    return render(
        request,
        'items/items_list.html', 
        {
            'items': pattern.pattern_items.all(),
            'top_bar': True,
            'collection_name': f'{pattern.name} Skins'
        }
    )
    


def item(request, id):
    item = Item.objects.get_object_or_404(id=id, accepted=True)

    return render(request, 'items/item.html', {'item': item, 'wears': ['fn', 'mw', 'ft', 'ww', 'bs']})


@login_required
def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.added_by = Profile.objects.get(user=request.user)
            data.save()
            if data.subcategory and data.pattern:
                item_name = f'{data.subcategory.name} | {data.pattern.name}'
            else:
                item_name = data.name
            return render(request, 'items/item_added.html', {'item_name': item_name})
    else:
        form = AddItemForm()

    return render(request, 'items/add_item.html', {'form': form})
