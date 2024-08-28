import json

from django.http import JsonResponse

from cdp_db_site_app.views.api.add_edit_disc import add_edit_disc


def json_add_edit_disc(request, position):
    body = json.loads(request.body)
    image = None
    group = None
    try:
        group = body["disc"]["group"]
    except KeyError:
        pass
    try:
        image = body["disc"]["image"]
    except KeyError:
        pass

    # Return the disc as JSON
    return JsonResponse(
        {
            "created_disc": add_edit_disc(position, body["disc"]["title"], image, group).as_json()
        }
    )