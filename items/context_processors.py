from items.models import Category


def category(request):
    return {'categories': Category.objects.all()}