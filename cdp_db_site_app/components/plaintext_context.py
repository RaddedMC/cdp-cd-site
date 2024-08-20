from cdp_db_site import settings
from cdp_db_site_app.components.titlebar_context import titlebar_context
from cdp_db_site_app.models import Disc


def plaintext_context(response_text, page_name, page_link):
    return dict(titlebar_context(), **{
        "response_text": response_text,
        "page_name": page_name,
        "page_link": page_link
    })