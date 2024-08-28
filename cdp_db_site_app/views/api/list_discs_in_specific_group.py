from django.http import JsonResponse

from cdp_db_site_app.models import Disc

# List all discs in a specific group
def list_discs_in_specific_group(request, group):
    group_discs = Disc.objects.filter(group=group)
    return JsonResponse({"group_discs_json": [disc.as_json() for disc in group_discs]})