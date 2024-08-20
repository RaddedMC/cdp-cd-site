import json
from json import JSONDecodeError

import django.core.exceptions
from django.http import HttpResponse, JsonResponse
from django.template import loader

from cdp_db_site import settings
from cdp_db_site_app.models import Group, Disc

### --- LIST INFO --- ###
# List all info from discs
def list_all_discs(request):
    all_discs = Disc.objects.all()
    return JsonResponse({"all_discs_json": [disc.as_json() for disc in all_discs]})

# List info from specific disc
def list_specific_disc(request, position):
    disc = Disc.objects.get(position=position)
    return JsonResponse({"single_disc_json": disc.as_json()})

# List all groups
def list_all_groups(request):
    all_groups = Group.objects.all()
    return JsonResponse({"all_groups_json": [group.as_json() for group in all_groups]})

# List all discs in a specific group
def list_discs_in_specific_group(request, group):
    group_discs = Disc.objects.filter(group=group)
    return JsonResponse({"group_discs_json": [disc.as_json() for disc in group_discs]})


### --- MANAGE GROUPS --- ###
# Create group
def create_group(request):
    body_as_json = json.loads(request.body)
    new_group = Group(title=body_as_json["group"]["title"], color=body_as_json["group"]["color"])
    new_group.save()

    return JsonResponse({"created_group": new_group.as_json()})

# Edit group
def edit_group(request, group):
    group_original = Group.objects.get(id=group)
    body_as_json = json.loads(request.body)
    if body_as_json["group"]["title"]:
        group_original.title = body_as_json["group"]["title"]
    if body_as_json["group"]["color"]:
        group_original.color = body_as_json["group"]["color"]
    group_original.save()
    return JsonResponse({"edited_group": group_original.as_json()})

# Remove group
def remove_group(request, group):
    Group.objects.get(id=group).delete()
    return HttpResponse("Group deleted successfully")


### --- MANAGE DISCS --- ###
# Add/Edit disc
def add_edit_disc(position, title, image = None, group_id = None):
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
    disc.image = image

    # If there is a group, set it
    # Otherwise set to null
    if not group_id or group_id == "null":
        disc.group = None
    else:
        try:
            disc.group = Group.objects.get(id=group_id)
        except KeyError:
            # A group that does not exist was given
            disc.group = None

    # Save the disc
    disc.save()

    return disc

def json_add_edit_disc(request, position):
    body = json.loads(request.body)
    image = None
    group = None
    try:
        group = body["disc"]["group"]
    except KeyError:
        pass
    try:
        image = body["disc"]["image"]
    except KeyError:
        pass

    # Return the disc as JSON
    return JsonResponse(
        {
            "created_disc": add_edit_disc(position, body["disc"]["title"], image, group).as_json()
        }
    )

# Remove disc
def remove_disc(request, position):
    template = loader.get_template('cdp_db_site_app/plaintext_responses.html');
    context = {
        "disc_count": Disc.objects.all().count(),
        "disc_capacity": settings.CDP_SIZE,
        "response_text": "Disc deleted successfully",
        "page_name": "home",
        "page_link": f"/{position}"
    }

    Disc.objects.get(position=position).delete()
    return HttpResponse(template.render(context, request))


### --- CONTROL COMMAND --- ###
# Send control command
def send_control_command(request, position):
    # TODO: implement me
    pass