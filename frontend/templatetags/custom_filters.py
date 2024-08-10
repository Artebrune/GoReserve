from django import template

register = template.Library()

@register.filter
def is_pdf(file_field):
    return file_field.name.lower().endswith('.pdf')