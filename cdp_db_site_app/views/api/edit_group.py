import json

from django.http import JsonResponse

from cdp_db_site_app.models import Group

# Edit group
def edit_group(request, group):
    group_original = Group.objects.get(id=group)
    body_as_json = json.loads(request.body)
    if body_as_json["group"]["title"]:
        group_original.title = body_as_json["group"]["title"]
    if body_as_json["group"]["color"]:
        group_original.color = body_as_json["group"]["color"]
    group_original.save()
    return JsonResponse({"edited_group": group_original.as_json()})