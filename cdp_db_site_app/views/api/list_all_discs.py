from django.http import JsonResponse

from cdp_db_site_app.models import Disc

# List all info from discs
def list_all_discs(request):
    all_discs = Disc.objects.all()
    return JsonResponse({"all_discs_json": [disc.as_json() for disc in all_discs]})