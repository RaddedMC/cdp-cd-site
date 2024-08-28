import json

from django.http import JsonResponse

from cdp_db_site_app.models import Group


# Create group
def create_group(request):
    body_as_json = json.loads(request.body)
    new_group = Group(title=body_as_json["group"]["title"], color=body_as_json["group"]["color"])
    new_group.save()

    return JsonResponse({"created_group": new_group.as_json()})