import django.core.exceptions
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.template import loader

from cdp_db_site import settings
from cdp_db_site_app.components.disc_carousel_context import disc_carousel_context
from cdp_db_site_app.forms.DiscForm import DiscForm
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
        form = DiscForm(request.POST)
        # Validate
        if form.is_valid():
            success_template = loader.get_template('cdp_db_site_app/plaintext_responses.html');
            context = {
                "disc_count": Disc.objects.all().count(),
                "disc_capacity": settings.CDP_SIZE,
                "response_text": "Disc updated successfully",
                "page_name": "home",
                "page_link": f"/{position}"
            }

            return HttpResponse(success_template.render(context, request))
        else:
            # If the form data is invalid we'll just send them the same form again
            pass

    # If this is a GET or any other method, we should create a blank form
    else:
        form = DiscForm()

    return disc_carousel_context(request, position, "edit", form)

# [OLD/remove me] sent on completion of form
# def form_add_edit_disc(request, position):
#     form = QueryDict(request.body, mutable=False)
#     add_edit_disc(position, form["title"], form["image"], form["group"])
#
#     template = loader.get_template('cdp_db_site_app/plaintext_responses.html');
#     context = {
#         "disc_count": Disc.objects.all().count(),
#         "disc_capacity": settings.CDP_SIZE,
#         "response_text": "Disc updated successfully",
#         "page_name": "home",
#         "page_link": f"/{position}"
#     }
#
#     return HttpResponse(template.render(context, request))