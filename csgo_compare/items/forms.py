from django import forms
from .models import Item
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class AddItemForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

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
            'subcategory',
            'rarity',
            'pattern',
            'collection'
        ]
