from django.shortcuts import render
from items.models import Item
from random import choice


def home(request):
    pks = Item.objects.filter(accepted=True).values_list('pk', flat=True)

    items = []
    if len(pks) > 0:
        while len(items) < 6:
            random_pk = choice(pks)
            item = Item.objects.get(id=random_pk)
            if item not in items:
                items.append(item)

    return render(request, 'base/home.html', {'items': items})
