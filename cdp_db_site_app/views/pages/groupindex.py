import django
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from cdp_db_site import settings
from cdp_db_site_app.components.plaintext_context import plaintext_context
from cdp_db_site_app.components.titlebar_context import titlebar_context
from cdp_db_site_app.models import Disc, Group


# Group list page

def groupindex(request, groupid, position=1):
    # Get all discs in this group
    discs_in_group = Disc.objects.filter(group = groupid)
    # If there are no discs, just return a text page
    if len(discs_in_group) == 0:
        template = loader.get_template('cdp_db_site_app/plaintext_responses.html');
        context = plaintext_context("There are no discs in group " + Group.objects.get(id=groupid).title, "home", f"/{position}")
        return HttpResponse(template.render(context, request))

    # Otherwise prepare a carousel manually
    # If the set position does not match any discs, change it to the first disc in the group's position
    if len(discs_in_group.filter(position=position)) == 0:
        position = discs_in_group[0].position

    # First find the index of the disc in the current position to set up next_scrolls
    current_disc_index = 0
    for index, item in enumerate(discs_in_group):
        if item.position == position:
            current_disc_index = index
            break

    next_scrolls = [
        discs_in_group[(current_disc_index + 1) % len(discs_in_group)].position,
        discs_in_group[(current_disc_index - 1) % len(discs_in_group)].position,
        discs_in_group[(current_disc_index + 50) % len(discs_in_group)].position,
        discs_in_group[(current_disc_index - 50) % len(discs_in_group)].position,
    ]

    # If there are 9 discs in the group, just return each disc.
    discs_json = []
    if len(discs_in_group) <= 9:
        for disc in discs_in_group:
            disc_json = disc.as_json()

            # If the disc has no image, set the empty image
            if not disc_json["image"]:
                disc_json["image"] = settings.HOMEPAGE_BLANK_DISC_ASSET

            # Retrieve full group info from disc group ID, if it has a group
            try:
                disc_group = Group.objects.get(id=disc_json["group"])
                disc_json["group"] = disc_group.as_json()

            # If it is a null group, set the disc JSON group to null
            except django.core.exceptions.ObjectDoesNotExist:
                disc_json["group"] = None

            # Switch the image to a transform if necessary
            if disc.position < position:
                disc_json["image"] = disc_json["image"][0:disc_json["image"].find(".")] + "_left" + disc_json["image"][disc_json["image"].find("."):]
            elif disc.position > position:
                disc_json["image"] = disc_json["image"][0:disc_json["image"].find(".")] + "_right" + disc_json["image"][
                                                                                      disc_json["image"].find("."):]
            else:
                current_disc = disc_json
            discs_json.append(disc_json)


    # If there are more than 9 discs, retrieve the current discs and 4 discs before/after.
    # Not the DRYest approach, but it's fine
    else:
        for i in range(-4, 5):
            disc_json = discs_in_group[(i + current_disc_index) % len(discs_in_group)].as_json()

            # If the disc has no image, set the empty image
            if not disc_json["image"]:
                disc_json["image"] = settings.HOMEPAGE_BLANK_DISC_ASSET

            # Retrieve full group info from disc group ID, if it has a group
            try:
                disc_group = Group.objects.get(id=disc_json["group"])
                disc_json["group"] = disc_group.as_json()

            # If it is a null group, set the disc JSON group to null
            except django.core.exceptions.ObjectDoesNotExist:
                disc_json["group"] = None

            # Switch the image to a transform if necessary
            if i < 0:
                disc_json["image"] = disc_json["image"][0:disc_json["image"].find(".")] + "_left" + disc_json["image"][disc_json["image"].find("."):]
            elif i > 0:
                disc_json["image"] = disc_json["image"][0:disc_json["image"].find(".")] + "_right" + disc_json["image"][disc_json["image"].find("."):]
            else:
                current_disc = disc_json
            discs_json.append(disc_json)

    context = dict(titlebar_context(searchable=True),**{
        "next_scrolls": next_scrolls,
        "discs": discs_json,
        "current_disc": current_disc,
        "group": current_disc["group"],
        "page_prefix": f"/group/{groupid}/disc",
        "scrollable": True,
        "group_length": len(discs_in_group)
    })

    return render(request, "cdp_db_site_app/group.html", context)