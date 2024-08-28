from django.http import JsonResponse

from cdp_db_site_app.models import Disc

# List info from specific disc
def list_specific_disc(request, position):
    disc = Disc.objects.get(position=position)
    return JsonResponse({"single_disc_json": disc.as_json()})