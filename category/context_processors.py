from .models import Category
from store.models import Color, Size

def menu_links(request):
    links = Category.objects.all()
    links_Color = Color.objects.all()
    links_Size = Size.objects.all()
    return dict(links=links,links_Color=links_Color, links_Size=links_Size)
