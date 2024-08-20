import django.core.exceptions
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.template import loader

from cdp_db_site import settings
from cdp_db_site_app.components.disc_carousel_context import disc_carousel_context
from cdp_db_site_app.components.plaintext_context import plaintext_context
from cdp_db_site_app.forms.DiscForm import DiscForm
from cdp_db_site_app.models import Disc
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
                "group": disc.group.pk if disc.group != None else "null",
                "image": disc.image.name
            })
        # If the disc does not exist, create a blank form
        except django.core.exceptions.ObjectDoesNotExist:
            form = DiscForm()


    context = disc_carousel_context(position, False, "edit/")
    context["form"] = form
    return render(request, "cdp_db_site_app/edit.html", context)
