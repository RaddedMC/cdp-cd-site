# List all groups
from django.http import JsonResponse

from cdp_db_site_app.models import Group


def list_all_groups(request):
    all_groups = Group.objects.all()
    return JsonResponse({"all_groups_json": [group.as_json() for group in all_groups]})