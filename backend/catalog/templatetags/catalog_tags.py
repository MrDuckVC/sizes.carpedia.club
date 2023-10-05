from django import template

from catalog.models import CategoryGroup, Category


register = template.Library()


@register.simple_tag
def get_category_groups():
    """
    Returns a list of category groups.

    :return: List of category groups.
    """
    return CategoryGroup.objects.all()


@register.simple_tag
def get_categories(category_group: CategoryGroup = None):
    """
    Returns a list of categories for the specified category group or all categories if category group is not specified.

    :param category_group: Category group to filter categories by.
    :return: List of categories.
    """
    if category_group:
        return Category.objects.filter(category_group=category_group)
    return Category.objects.all()


@register.inclusion_tag("catalog/templatetags/categories_cards.html")
def show_categories_cards(category_group: CategoryGroup = None):
    """
    Returns a list of categories for the specified category group or all categories if category group is not specified.

    :param category_group: Category group to filter categories by.
    :return: List of categories.
    """
    if category_group:
        return {"categories": Category.objects.filter(category_group=category_group)}
    return {"categories": Category.objects.all()}


@register.inclusion_tag("catalog/templatetags/auto_part_row.html")
def auto_part_row(auto_part):
    """
    Returns a list of categories for the specified category group or all categories if category group is not specified.

    :param category_group: Category group to filter categories by.
    :return: List of categories.
    """
    return {"auto_part": auto_part}


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
