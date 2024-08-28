from django.shortcuts import render

from cdp_db_site_app.components.disc_carousel_context import disc_carousel_context

# Main disc list page
def index(request, position=1):
    return render(request, "cdp_db_site_app/index.html", disc_carousel_context(position, scrollable = True, searchable = True))