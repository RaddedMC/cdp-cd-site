from django.shortcuts import render

from cdp_db_site_app.components.plaintext_context import plaintext_context
from cdp_db_site_app.components.titlebar_context import titlebar_context
from cdp_db_site_app.forms.GroupForm import GroupForm
from cdp_db_site_app.models import Group

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