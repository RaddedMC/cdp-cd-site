from django.http import HttpResponse
from django.template import loader

from cdp_db_site_app.components.plaintext_context import plaintext_context
from cdp_db_site_app.models import Group

# Remove group
def remove_group(request, group):
    template = loader.get_template('cdp_db_site_app/plaintext_responses.html');
    context = plaintext_context("Group deleted successfully. Any games with this group will now be NO GROUP.", "home", "/")

    Group.objects.get(id=group).delete()
    return HttpResponse(template.render(context, request))