import django.core.exceptions
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.template import loader

from cdp_db_site import settings
from cdp_db_site_app.components.disc_carousel_context import disc_carousel_context
from cdp_db_site_app.components.plaintext_context import plaintext_context
from cdp_db_site_app.components.titlebar_context import titlebar_context
from cdp_db_site_app.forms.DiscForm import DiscForm
from cdp_db_site_app.forms.GroupForm import GroupForm
from cdp_db_site_app.models import Disc, Group
from cdp_db_site_app.views.api import add_edit_disc


# Main disc list page
def index(request, position=1):
    return render(request, "cdp_db_site_app/index.html", disc_carousel_context(position, scrollable = True))

# Disc edit page
def edit(request, position):
    # If this is a POST we need to submit the form data
    if request.method == "POST":
        # Populate a form object with data
        form = DiscForm(request.POST, request.FILES)
        # If the form is valid, show a success screen
        # If not, they will be returned to the form page
        if form.is_valid():
            # Handle saving disc
            add_edit_disc(position, form.cleaned_data["title"], form.cleaned_data["image"], form.cleaned_data["group"], form.cleaned_data[
                "changeimage"])
            return render(request, 'cdp_db_site_app/plaintext_responses.html', plaintext_context("Disc changed successfully", "home", f"/{position}"))

    # If this is a GET or any other method, we are starting with a fresh form
    else:
        # If this disc position exists already we should prefill the data
        try:
            disc = Disc.objects.get(position=position)
            form = DiscForm({
                "title": disc.title,
                "group": disc.group.pk if disc.group != None else None,
                "image": disc.image.name
            })
        # If the disc does not exist, create a blank form
        except django.core.exceptions.ObjectDoesNotExist:
            form = DiscForm()

    #print(form)
    context = disc_carousel_context(position, False, "edit/")
    context["form"] = form
    return render(request, "cdp_db_site_app/edit.html", context)

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

    context = dict(titlebar_context(),**{
        "next_scrolls": next_scrolls,
        "discs": discs_json,
        "current_disc": current_disc,
        "group": current_disc["group"],
        "page_prefix": f"/group/{groupid}/disc",
        "scrollable": True,
        "group_length": len(discs_in_group)
    })

    return render(request, "cdp_db_site_app/group.html", context)

# Group add/edit page
def groupchange(request, groupid=-1):
    def savegroup(title, color):
        if groupid < 0:
            # Group does not exist. create a new one!
            group = Group(title=title, color=color)
        else:
            # The group does exist (they navigated to it)
            group = Group.objects.get(id=groupid)
            group.title = title
            group.color = color

        group.save()

    # If this is a POST we need to submit form data
    if request.method == "POST":
        # Populate a form with data
        form = GroupForm(request.POST)
        # If the form is valid, show a success screen
        # If not, they will be returned to the form page
        if form.is_valid():
            # Handle saving group
            savegroup(form.cleaned_data["title"], form.cleaned_data["color"])
            return render(request, 'cdp_db_site_app/plaintext_responses.html',
                          plaintext_context("Groups changed successfully", "home", f"/1"))

    # If this is a GET request, we neeed to send them a form
    else:
        if groupid < 0:
            # They are creating a new group. Give them a blank form!
            form = GroupForm()
        else:
            # They are editing an existing group. Get the relevant info!
            existing_group = Group.objects.get(id=groupid)
            form = GroupForm({
                "title": existing_group.title,
                "color": existing_group.color
            })

    context = dict(titlebar_context(), **{
        "form": form,
        "groupid": groupid
    })

    return render(request, "cdp_db_site_app/group_edit.html", context)