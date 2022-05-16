from django.shortcuts import render
from items.models import Category, Subcategory, Container, Item


def stat(request):
    return render(request, 'info/stat.html',
                  {
                      'total_items': len(Item.objects.filter(accepted=True).all()),
                      'total_submited_items': len(Item.objects.all()),
                      'total_pending_items': len(Item.objects.filter(accepted=False).all()),
                      'subcats': Subcategory.objects.all(),
                  })


def about(request):
    return render(request, 'info/about.html')