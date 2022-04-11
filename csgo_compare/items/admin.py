from django.contrib import admin
from .models import (
    Category,
    Subcategory,
    Rarity,
    Update,
    Collection,
    Event,
    DropStatus,
    Container,
    Item
)


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Rarity)
admin.site.register(Update)
admin.site.register(Collection)
admin.site.register(Event)
admin.site.register(DropStatus)
admin.site.register(Container)
admin.site.register(Item)