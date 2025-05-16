from django import template
from navigation.models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('navigation/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path

    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_items': []}

    all_items = MenuItem.objects.filter(menu=menu).select_related('parent')

    # Метки
    for item in all_items:
        resolved_url = item.get_absolute_url()
        item.resolved_url = resolved_url
        item.is_active = (resolved_url == current_path)
        item.is_ancestor = False
        item.show_children = False

    # Активный пункт
    active_item = next((item for item in all_items if item.is_active), None)

    # Отметить родителей и показать подуровень
    if active_item:
        parent = active_item.parent
        while parent:
            parent.is_ancestor = True
            parent.show_children = True
            parent = parent.parent
        active_item.show_children = True

    root_items = [item for item in all_items if item.parent is None]

    return {
        'menu_items': root_items,
        'request': request,
    }