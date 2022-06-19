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
            'added_by',
            'subcategory',
            'rarity',
            'collection'
        ]
