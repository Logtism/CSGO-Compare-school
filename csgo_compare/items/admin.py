from django.contrib import admin
from .models import (
    Category,
    Subcategory,
    Rarity,
    Update,
    KnifeCollection,
    Collection,
    Tournament,
    Container,
    Pattern,
    Item
)


# Adding all the items model to the django admin page
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Rarity)
admin.site.register(Update)
admin.site.register(KnifeCollection)
admin.site.register(Collection)
admin.site.register(Container)
admin.site.register(Tournament)
admin.site.register(Pattern)
admin.site.register(Item)
