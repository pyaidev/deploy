import os

from django import template
from django.template import Context, Template

from config.settings import BASE_DIR, GOOGLE_MAPS_KEY

register = template.Library()


# Creating a simple template tag
@register.simple_tag
def mediapath(format_string):
    # This tag returns a string representing the media path for a given format_string.
    # It's designed to be used in templates like: {% mediapath "images/my_image.jpg" %}
    return f'/media/{format_string}'


# Creating a template filter
@register.filter
def mediapath_filter(text):
    # This filter appends "/media/" to the beginning of the input text.
    # It's designed to be used in templates like: {{ "images/my_image.jpg" | mediapath_filter }}
    return f'/media/{text}'


@register.filter
def get_item(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return "Key not found"


@register.filter
def replace_figure_tags(input_html, material_photos_list):
    # Regular expression to search for <p> tags with text like '{figure-<any number>}'
    import re

    #pattern = r'<p\b[^>]*>\s*{figure-(\d+)}\s*</p>'
    pattern = r'{figure-(\d+)}'


    matches = re.finditer(pattern, input_html)

    # Read file contents
    with open(os.path.join(BASE_DIR,
                           'education_content/templates/education_content/includes/inc_material_photo_card_for_material_detail.html'),
              'r') as file:
        template_content_prepared = file.read()

    material_photos_by_pk = {}
    for material_photo in material_photos_list:
        material_photos_by_pk[material_photo.pk] = material_photo

    # Create a Context object if you need to pass additional variables to the template
    context = Context({'material_photos_by_pk': material_photos_by_pk,
                       'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY})

    # We go through all the matches found
    for match in matches:

        figure_number = match.group(1)

        template_content = template_content_prepared

        # Replace <CURRENT_PK> with figure_number value
        template_content = template_content.replace('<CURRENT_PK>', figure_number)

        # Create a Template object
        template = Template(template_content)

        # Render template
        rendered_template = template.render(context)

        # Replace the found tag in input_html with the result of the template rendering
        input_html = input_html.replace(match.group(0), rendered_template)

    return input_html
