import django

from cdp_db_site_app.models import Disc

# Add/Edit disc
def add_edit_disc(position, title, image = None, group_obj = None, change_image = False):
    # Is there a disc at that position?
    # If so use it to prefill fields
    try:
        previous_disc = Disc.objects.get(position=position)
    except django.core.exceptions.ObjectDoesNotExist:
        previous_disc = Disc()

    # Set the position
    disc = previous_disc
    disc.position = position

    # Set the new title [MANDATORY]
    disc.title = title

    # If there is an image, set it
    # Otherwise set to null
    # Skip this section if keep image is set
    if change_image:
        disc.image = image

    # If there is a group, set it
    # Otherwise set to null
    if not group_obj or group_obj == "null":
        disc.group = None
    else:
        disc.group = group_obj

    # Save the disc
    disc.save()

    return disc