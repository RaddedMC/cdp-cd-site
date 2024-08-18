import django.core.exceptions
from django.http import HttpResponse
from django.template import loader

from cdp_db_site import settings
from cdp_db_site_app.models import Disc, Group

def get_scroll_number(base_position, offset):
    pos = base_position+offset
    if pos > 300:
        return pos - 300
    elif pos <= 0:
        return 300+pos
    else: return pos

def index(request, position=1):

    # Populate disc information
    discs = []

    # Grab 7 discs (current position plus three left and three right
    for i in range(-3, 4):
        # Calculate the position of the 3 left and right
        pos = get_scroll_number(position, i)

        print("Disc " + str(pos))

        # Retrieve a disc at position, if it exists
        try:
            disc = Disc.objects.get(position=pos).as_json()

        # If there is no disc at the position, add a generic blank disc
        except django.core.exceptions.ObjectDoesNotExist:
            disc = ({
                "title": "_",
                "position": pos,
                "image": settings.HOMEPAGE_NO_DISC_ASSET,
                "group": None
            })

        print("Disc original data")
        print(disc)

        # If the disc has no image, set the empty image
        if not disc["image"]:
            disc["image"] = settings.HOMEPAGE_BLANK_DISC_ASSET

        print("Disc after swapping image")
        print(disc)

        # Retrieve full group info from disc group ID, if it has a group
        try:
            disc_group = Group.objects.get(id=disc["group"])
            disc["group"] = disc_group.as_json()

        # If it is a null group, set the disc JSON group to null
        except django.core.exceptions.ObjectDoesNotExist:
            disc["group"] = None

        # Add to the disc list
        print("Final disc")
        print(disc)
        discs.append(disc)
        print()

    # Retrieve all the groups as JSON
    groups = [group.as_json() for group in Group.objects.all()]

    # Populate the template
    template = loader.get_template("cdp_db_site_app/index.html")
    context = {
        "discs": discs,
        "groups": groups,
        "current_disc": discs[3],
        "disc_count": Disc.objects.all().count(),
        "disc_capacity": settings.CDP_SIZE
    }

    # Render and return the template
    return HttpResponse(template.render(context, request))