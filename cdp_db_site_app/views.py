import json
from json import JSONDecodeError

import django.core.exceptions
from django.core import serializers
from django.http import HttpResponse, JsonResponse

from cdp_db_site_app.models import Group, Disc

# List all info from discs [GET] GOOD
def list_all_discs(request):
    all_discs = Disc.objects.all()
    return JsonResponse({"all_discs_json": [disc.as_json() for disc in all_discs]})

# List info from specific disc [GET] GOOD
def list_specific_disc(request, position):
    disc = Disc.objects.get(position=position)
    return JsonResponse({"single_disc_json": disc.as_json()})

# List all groups [GET] GOOD
def list_all_groups(request):
    all_groups = Group.objects.all()
    return JsonResponse({"all_groups_json": [group.as_json() for group in all_groups]})

# List all discs in a specific group [GET]
def list_discs_in_specific_group(request, group):
    group_discs = Disc.objects.filter(group=group)
    return JsonResponse({"group_discs_json": [disc.as_json() for disc in group_discs]})


# Create group [POST] GOOD
def create_group(request):
    body_as_json = json.loads(request.body)
    new_group = Group(title=body_as_json["group"]["title"], color=body_as_json["group"]["color"])
    new_group.save()

    return JsonResponse({"created_group": new_group.as_json()})


# Edit group [PUT] GOOD
def edit_group(request, group):
    group_original = Group.objects.get(id=group)
    body_as_json = json.loads(request.body)
    if body_as_json["group"]["title"]:
        group_original.title = body_as_json["group"]["title"]
    if body_as_json["group"]["color"]:
        group_original.color = body_as_json["group"]["color"]
    group_original.save()
    return JsonResponse({"edited_group": group_original.as_json()})

# Remove group [DELETE] GOOD
def remove_group(request, group):
    Group.objects.get(id=group).delete()
    return HttpResponse("Group deleted successfully")


# Add/Edit disc [PUT/POST] GOOD
def add_edit_disc(request, position):
    # Retrieve body data
    body_as_json = json.loads(request.body)

    # Is there a disc at that position?
    # If so use it to prefill fields
    try:
        previous_disc = Disc.objects.get(position=position)
    except django.core.exceptions.ObjectDoesNotExist:
        previous_disc = Disc()

    # Get the input position [MANDATORY]
    previous_disc.position = position

    # Get the new title [MANDATORY]
    previous_disc.title = body_as_json["disc"]["title"]

    # If it was input get the image
    # Otherwise set it as null
    try:
        previous_disc.image = body_as_json["disc"]["image"]
    except JSONDecodeError:
        previous_disc.image = None
    except KeyError:
        previous_disc.image = None

    # If it was input get the group id
    # Otherwise set it as null
    try:
        previous_disc.group = Group.objects.get(id=body_as_json["disc"]["group"])
    except JSONDecodeError:
        previous_disc.group = None
    except KeyError:
        previous_disc.group = None

    # Save the changes
    previous_disc.save()

    # Return the disc as JSON
    return JsonResponse({"created_disc":previous_disc.as_json()})


# Remove disc [DELETE] GOOD
def remove_disc(request, position):
    Disc.objects.get(position=position).delete()
    return HttpResponse("Disc deleted successfully")


# Send control command [GET]
def send_control_command(request, position):
    # TODO: implement me
    pass