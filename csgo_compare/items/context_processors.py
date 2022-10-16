from items.models import Category


def category(request):
    '''
    Return all the categories in the database so
    they can be used in templates
    '''
    return {'categories': Category.objects.all()}
