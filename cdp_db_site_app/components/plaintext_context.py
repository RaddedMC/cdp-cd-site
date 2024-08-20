from cdp_db_site import settings
from cdp_db_site_app.models import Disc


def plaintext_context(response_text, page_name, page_link):
    return {
        "disc_count": Disc.objects.all().count(),
        "disc_capacity": settings.CDP_SIZE,
        "response_text": response_text,
        "page_name": page_name,
        "page_link": page_link
    }