from django.contrib import admin
from .models import (
    Category,
    Subcategory,
    Rarity,
    Collection,
    Container,
    Item
)


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Rarity)
admin.site.register(Collection)
admin.site.register(Container)
admin.site.register(Item)
