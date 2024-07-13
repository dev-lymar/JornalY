from django import template

register = template.Library()


@register.filter(name='addclass')
def addclass(field, css):
    classes, attrs = css.split('&')
    attrs = attrs.strip().split()
    class_dict = {'class': classes.strip()}
    for attr in attrs:
        key, value = attr.split('=')
        class_dict[key.strip()] = value.strip()
    return field.as_widget(attrs=class_dict)
