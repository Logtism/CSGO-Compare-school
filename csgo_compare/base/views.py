from django.shortcuts import render
from items.models import Item
from random import choice


def home(request):
    '''
    Home page of the website displaying a random selection of items.
    '''
    # Getting a list of item id's
    # Using flat as only one value in value list
    pks = Item.objects.filter(accepted=True).values_list('pk', flat=True)

    items = []
    # Checking that the list of id's has items in it
    if len(pks) > 0:
        # While items does not have 9 items continue looping
        while len(items) < 9:
            # Picking a random item and checking it has not already been
            # picked if it hasn't add it to list of random items
            random_pk = choice(pks)
            item = Item.objects.get(id=random_pk)
            if item not in items:
                items.append(item)

    return render(
        request,
        'items/items_list.html',
        {
            'items': items,
            'top_bar': False
        }
    )
