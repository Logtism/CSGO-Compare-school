from django.db import models
from accounts.models import Profile
import os


class Category(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return f'{self.name}'
    
    
    
class Subcategory(models.Model):
    name = models.CharField(max_length=150)
    icon = models.ImageField(upload_to=os.path.join('imgs', 'collection', 'small'))
    icon_large = models.ImageField(upload_to=os.path.join('imgs', 'collection', 'large'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    
    def __str__(self):
        return f'{self.name}'
    

class Rarity(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=25)
    
    def __str__(self):
        return f'{self.name}'

    
class Collection(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to=os.path.join('imgs', 'collection'))
    
    def __str__(self):
        return f'{self.name}'
    
    
class Container(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to=os.path.join('imgs', 'container'))
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name}'
  
  
def get_upload_to_path(self, file_name):
    return f'imgs/item/{self.subcategory.name}/{file_name}'

    
class Item(models.Model):
    name = models.CharField(max_length=300)
    icon = models.ImageField(upload_to=get_upload_to_path)
    
    skinport_id = models.CharField(max_length=300, null=True, blank=True)
    
    lowest_float = models.FloatField(null=True, blank=True)
    highest_float = models.FloatField(null=True, blank=True)
    stattrak = models.BooleanField(default=False)
    souvenir = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    added_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='items')
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE, null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True, related_name='collection_items')
    
    class Meta:
        permissions = (
            ('can_view_item_sub', 'Can view new item submissions'),
            ('can_accept_item_sub', 'Can accept item submissions.'),
            ('can_decline_item_sub', 'Can decline item submissions'),
        )
    
    def __str__(self):
        return f'{self.name}'