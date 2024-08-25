import django

from cdp_db_site import settings
from cdp_db_site_app.components.titlebar_context import titlebar_context
from cdp_db_site_app.models import Disc, Group

# Calculate what position the disc player is in given a base position and offset
# Essentially just account for the circular nature of the disc tray
def get_scroll_number(base_position, offset, closest_disc = False):
    # print(f"The user asked for offset {offset} from base position {base_position}" + (" with closest disc" if closest_disc else ""))
    pos = base_position + offset
    if pos > 300:
        pos = pos - 300
    elif pos <= 0:
        pos = 300 + pos
    # print(("Without considering closest disc, " if closest_disc else "") + f"the position is {pos}")

    if closest_disc:
        # If going up
        if offset > 0:
            # print(f"We went up! We need to find the disc with the lowest number from {base_position} to {settings.CDP_SIZE}")
            # We need to find the disc with the lowest number from base_position to max
            discs_above = Disc.objects.filter(position__gt=base_position).order_by("position")
            # print("The discs in that range: ", discs_above)
            if len(discs_above) > 0:
                # print(f"Found a disc at position {discs_above[0].position}")
                return discs_above[0].position
            # If there is none, overscroll to find the disc with the lowest number from 0 to (ex)base_position
            else:
                # print(f"No disc above! Checking in overscroll...")
                discs_above_overscroll = Disc.objects.filter(position__gt=0, position__lt=base_position).order_by("position")
                # print("The discs in overscroll: ", discs_above_overscroll)
                if len(discs_above_overscroll) > 0:
                    # print(f"Found a disc at position {discs_above_overscroll[0].position}")
                    return discs_above_overscroll[0].position
            # If none there, return pos
        # If going down
        else:
            # print(f"We went down! We need to find the disc with the lowest number from {base_position} to 0")
            # We need to find the disc with the highest number from base_position to 0
            discs_below = Disc.objects.filter(position__lt=base_position).order_by("-position")
            # print("The discs in that range: ", discs_below)
            if len(discs_below) > 0:
                # print(f"Found a disc at position {discs_below[0].position}")
                return discs_below[0].position
            # If there is none, overscroll to find the disc with the lowest number from max to (ex)base_position
            else:
                # print(f"No disc below! Checking in overscroll...")
                discs_below_overscroll = Disc.objects.filter(position__gt=base_position, position__lte=settings.CDP_SIZE).order_by(
                    "-position")
                # print("The discs in overscroll: ", discs_below_overscroll)
                if len(discs_below_overscroll) > 0:
                    # print(f"Found a disc at position {discs_below_overscroll[0].position}")
                    return discs_below_overscroll[0].position
            # If none there, return pos
    # if closest_disc:
    #     print("Couldn't find any there either. Just returning position.")
    return pos

# Pre-fill the disc carousel data and return a page containing a disc carousel
def disc_carousel_context(position, scrollable, page = ""):
    # Populate disc information
    discs = []

    # Grab 9 discs (current position plus three left and three right
    for i in range(-4, 5):
        # Calculate the position of the 3 left and right
        pos = get_scroll_number(position, i)


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


        # If the disc has no image, set the empty image
        if not disc["image"]:
            disc["image"] = settings.HOMEPAGE_BLANK_DISC_ASSET


        # Retrieve full group info from disc group ID, if it has a group
        try:
            disc_group = Group.objects.get(id=disc["group"])
            disc["group"] = disc_group.as_json()

        # If it is a null group, set the disc JSON group to null
        except django.core.exceptions.ObjectDoesNotExist:
            disc["group"] = None

        # Switch the image to a transform if necessary
        if i < 0:
            disc["image"] = disc["image"][0:disc["image"].find(".")] + "_left" + disc["image"][disc["image"].find("."):]
        elif i > 0 :
            disc["image"] = disc["image"][0:disc["image"].find(".")] + "_right" + disc["image"][disc["image"].find("."):]

        # Add to the disc list
        discs.append(disc)

    # Retrieve all the groups as JSON
    groups = [group.as_json() for group in Group.objects.all()]

    # Populate the template
    context = dict(titlebar_context(),**{
        "next_scrolls": [get_scroll_number(position, 4, closest_disc = True), get_scroll_number(position, -4, closest_disc = True),
                         get_scroll_number(position, 50), get_scroll_number(position, -50)],
        "discs": discs,
        "groups": groups,
        "current_disc": discs[4],
        "page_prefix": page,
        "scrollable": scrollable
    })

    # Render and return the template
    return context