from django.http.response import JsonResponse
import requests
from items.models import Item


def skinport(request, id):
    '''
    Get an items price from skinport.
    '''
    # Try get the item with id if not return an error
    try:
        item = Item.objects.get(id=id, accepted=True)
    except Item.DoesNotExist:
        return JsonResponse(
            {
                'success': False,
                'error_msg': 'Item id does not exist.'
            },
            status=404
        )

    prices = {'fn': 0, 'mw': 0, 'ft': 0, 'ww': 0, 'bs': 0, 'success': True}
    wears = {2: 'fn', 4: 'mw', 3: 'ft', 5: 'ww', 1: 'bs'}

    # Go though each wear and get the price for it
    for wear in wears:
        r = requests.get(
            (
                "https://skinport.com/api/browse/730"
                f"?{item.skinport_id}&sort=price&order=asc&exterior={wear}"
            ),
            headers={
                'Referer': 'https://skinport.com/api/browse/730',
                'Cookie': 'i18n=en; _csrf=-OYf7uAQmPZwniD-123456-p'
            }
        )
        # Checking that a price was returned
        if len(r.json()['items']) > 0:
            # Formating the price
            prices[wears[wear]] = r.json()['items'][0]['salePrice'] / 100

    return JsonResponse(prices)
