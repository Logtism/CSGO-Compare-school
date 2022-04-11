from django.db import models
from accounts.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=150)
    
    
class Subcategory(models.Model):
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=400, null=True)
    icon_large = models.CharField(max_length=400, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    

class Rarity(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=25)
    
    
class Update(models.Model):
    name = models.CharField(max_length=300)
    date = models.DateField()
    link = models.CharField(max_length=400)
    
    
class Collection(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=400)
    icon_large = models.CharField(max_length=400)
    
    
class Event(models.Model):
    name = models.CharField(max_length=200)
    
    

class DropStatus(models.Model):
    name = models.CharField(max_length=100)
    
    
class Container(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=400)
    icon_large = models.CharField(max_length=400)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    dropstatus = models.ForeignKey(DropStatus, on_delete=models.CASCADE, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    
    
class Item(models.Model):
    name = models.CharField(max_length=300)
    icon = models.CharField(max_length=400)
    icon_large = models.CharField(max_length=400)
    lowest_float = models.FloatField(null=True, blank=True)
    highest_float = models.FloatField(null=True, blank=True)
    stattrak = models.BooleanField(default=False)
    souvenir = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    added_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    update = models.ForeignKey(Update, on_delete=models.CASCADE)
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True)