from cdp_db_site import settings
from cdp_db_site_app.models import Disc


def titlebar_context(searchable = False):
    return {
        "disc_count": Disc.objects.all().count(),
        "disc_capacity": settings.CDP_SIZE,
        "searchable": searchable
    }