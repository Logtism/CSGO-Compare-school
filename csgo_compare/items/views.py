from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import Profile
from .models import Subcategory, Collection, Pattern, Item, Rarity
from .forms import AddItemForm


def sort_filter_items(request, data):
    '''
    Sort and filter a list of items.
    '''
    filter_options = {
        'rarity_cg': {'rarity': 1},
        'rarity_ig': {'rarity': 2},
        'rarity_ms': {'rarity': 3},
        'rarity_rs': {'rarity': 4},
        'rarity_cl': {'rarity': 5},
        'rarity_co': {'rarity': 6},
        'rarity_cn': {'rarity': 7},
        'rarity_hg': {'rarity': 8},
        'rarity_rm': {'rarity': 9},
        'rarity_ex': {'rarity': 10},
        'rarity_et': {'rarity': 11},
        'rarity_di': {'rarity': 12},
        'rarity_ep': {'rarity': 13},
        'rarity_su': {'rarity': 14},
        'rarity_ma': {'rarity': 15},
        'stattrak_y': {'stattrak': True},
        'stattrak_n': {'stattrak': False},
        'souvenir_y': {'souvenir': True},
        'souvenir_n': {'souvenir': False},
    }

    q_args = {}

    # Loop though each option and add it q_args that will
    # be used as filters in a later query
    for option in filter_options:
        query_value = request.GET.get(option, 0)
        try:
            int(query_value)
        except TypeError:
            continue
        if bool(int(query_value)):
            q_args[
                list(filter_options[option].keys())[0]
            ] = filter_options[option][list(filter_options[option].keys())[0]]

    # Creating a filter object
    query_filters = Q(**q_args, _connector=Q.OR)

    # Getting sorting setting
    sort_type = request.GET.get('sort_by', 0)

    # 0 age decening
    # 1 age asec
    # 2 rarity decs
    # 3 rarity decending

    # converting number to sort option
    if sort_type == '1':
        sort_by_value = '-id'
    elif sort_type == '2':
        sort_by_value = '-rarity'
    elif sort_type == '3':
        sort_by_value = 'rarity'
    else:
        sort_by_value = 'id'

    # Return the filtered and sorted items
    return data.filter(
        accepted=True
    ).filter(
        query_filters
    ).order_by(
        sort_by_value
    ).all()


def subcat(request, id):
    '''
    Display all the items in a subcategory.
    '''
    # Get all the items in the subcategory
    subcat_ = Subcategory.objects.get_object_or_404(id=id)
    # Sort and filter the items in subcategory
    subcat_items = sort_filter_items(request, subcat_.items)

    return render(
        request,
        'items/items_list.html',
        {
            'items': subcat_items,
            'top_bar': True,
            'rarity_filters': Rarity.objects.filter(
                item_type='weapon'
                ).order_by(
                    '-id'
                ).all(),
            'type_filters': {
                'stattrak_y': {'Stattrak': 'ffae39'},
                'stattrak_n': {'No Stattrak': '00000'},
                'souvenir_y': {'Souvenir': '00000'},
                'souvenir_n': {'No Souvenir': '00000'}
            },
            'collection_name': f'{subcat_.name} Skins'
        }
    )


def collection(request, id):
    '''
    Display all items in a collection.
    '''
    # Get all the items in the collection
    collection_ = Collection.objects.get_object_or_404(id=id)
    # Sort and filter the items in collection
    collectio_items = sort_filter_items(request, collection_.collection_items)
    return render(
        request,
        'items/items_list.html',
        {
            'items': collectio_items,
            'top_bar': True,
            'collection_name': f'{collection_.name}'
        }
    )


def pattern(request, id):
    '''
    Display all items with a pattern.
    '''
    # Get all the items with a pattern
    pattern_ = Pattern.objects.get_object_or_404(id=id)
    # Sort and filter with a pattern
    pattern_items = sort_filter_items(request, pattern_.pattern_items)
    return render(
        request,
        'items/items_list.html',
        {
            'items': pattern_items,
            'top_bar': True,
            'rarity_filters': Rarity.objects.filter(
                item_type='weapon'
            ).order_by(
                '-id'
            ).all(),
            'type_filters': {
                'stattrak_y': {'Stattrak': 'ffae39'},
                'stattrak_n': {'No Stattrak': '00000'},
                'souvenir_y': {'Souvenir': '00000'},
                'souvenir_n': {'No Souvenir': '00000'}
            },
            'collection_name': f'{pattern_.name} Skins'
        }
    )


def item(request, id):
    '''
    Give more detailed info about an item.
    '''
    # Get the item from the database or give a 404
    item = Item.objects.get_object_or_404(id=id, accepted=True)

    return render(
        request,
        'items/item.html',
        {
            'item': item,
            'wears': [
                'fn',
                'mw',
                'ft',
                'ww',
                'bs'
            ]
        }
    )


@login_required
def add_item(request):
    '''
    Give a form to add an item.
    '''
    if request.method == 'POST':
        # If the request is a post initialize form with post and file data
        # Need to pass file data as this forms has an image field
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            # If the form is valid add the user that added the item and
            # save the item to the database
            data = form.save(commit=False)
            data.added_by = Profile.objects.get(user=request.user)
            data.save()
            # Get the item's name depending on what data the item has
            if data.subcategory and data.pattern:
                item_name = f'{data.subcategory.name} | {data.pattern.name}'
            else:
                item_name = data.name
            # Return a page thanking the user for their contribution
            return render(
                request,
                'items/item_added.html',
                {
                    'item_name': item_name
                }
            )
    else:
        form = AddItemForm()

    return render(request, 'items/add_item.html', {'form': form})
