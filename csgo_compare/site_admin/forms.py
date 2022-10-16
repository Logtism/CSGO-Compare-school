from django import forms
from items.models import Item


class UpdateItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = [
            'name',
            'icon',
            'lowest_float',
            'highest_float',
            'stattrak',
            'souvenir',
            'steam_id',
            'buff_id',
            'bitskins_id',
            'skinport_id',
            'skinbaron_id',
            'broskins_id',
            'added_by',
            'subcategory',
            'rarity',
            'update',
            'pattern',
            'knife_collection',
            'collection'
        ]
