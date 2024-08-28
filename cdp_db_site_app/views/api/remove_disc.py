from django.http import HttpResponse
from django.template import loader

from cdp_db_site_app.components.plaintext_context import plaintext_context
from cdp_db_site_app.models import Disc

# Remove disc
def remove_disc(request, position):
    template = loader.get_template('cdp_db_site_app/plaintext_responses.html');
    context = plaintext_context("Disc deleted successfully", "home", f"/{position}")

    Disc.objects.get(position=position).delete()
    return HttpResponse(template.render(context, request))