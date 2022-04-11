from django import forms
from .models import Item


class AddItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = [
            'name',
            'icon',
            'icon_large',
            'lowest_float',
            'highest_float',
            'stattrak',
            'souvenir',
            'subcategory',
            'update',
            'rarity',
            'collection'
        ]