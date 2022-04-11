from django.shortcuts import render
from .models import Subcategory, Item


def items(request, id):
    subcat = Subcategory.objects.get_object_or_404(id=id)
    return render(request, 'items/items.html', {'subcat': subcat})


def item(request, id):
    item = Item.objects.get_object_or_404(id=id)
    return render(request, 'items/item.html', {'item': item})
