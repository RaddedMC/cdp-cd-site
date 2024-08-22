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
            add_edit_disc(position, form.cleaned_data["title"], form.cleaned_data["image"], form.cleaned_data["group"])
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

    print(form)
    context = disc_carousel_context(position, False, "edit/")
    context["form"] = form
    return render(request, "cdp_db_site_app/edit.html", context)

# Group list page
def groupindex(request, groupid, position=1):
    context = disc_carousel_context(position, scrollable = True, page=f"/group/{groupid}/disc")
    context["group"] = Group.objects.get(id=groupid).as_json()
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