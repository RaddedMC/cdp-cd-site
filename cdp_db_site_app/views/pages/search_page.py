from django.http import HttpResponse
from django.template import loader

from cdp_db_site import settings
from cdp_db_site_app.components.plaintext_context import plaintext_context
from cdp_db_site_app.components.titlebar_context import titlebar_context
from cdp_db_site_app.models import Disc, Group


def search_page(request):
    search_query = request.GET.get('search', None)
    group_filter = request.GET.get('group',None)

    if search_query is None or search_query == "":
        template = loader.get_template('cdp_db_site_app/plaintext_responses.html');
        context = plaintext_context("lol you searched for literally nothing", "home", "/")
        return HttpResponse(template.render(context, request))

    if group_filter is None or group_filter == "":
        discs_query = Disc.objects.filter(title__contains=search_query)
    else:
        discs_query = Disc.objects.filter(title__contains=search_query, group_id=int(group_filter))
        discs_group = Group.objects.get(id=int(group_filter))

    if len(discs_query) == 0:
        template = loader.get_template('cdp_db_site_app/plaintext_responses.html')
        context = plaintext_context(f"No results for {search_query}" if group_filter is None or group_filter == "" else f"No results for {search_query} in group {discs_group.title}", "home", "/")
        return HttpResponse(template.render(context, request))

    disc_result_json = [disc.as_json() for disc in discs_query]
    for index in range(len(disc_result_json)):
        if not disc_result_json[index]["image"]:
            disc_result_json[index]["image"] = settings.HOMEPAGE_BLANK_DISC_ASSET
        if disc_result_json[index]["group"]:
            disc_result_json[index]["group"] = Group.objects.get(id=disc_result_json[index]["group"]).as_json()

    template = loader.get_template("cdp_db_site_app/search.html")
    context = dict(titlebar_context(), **{
        "search_query": search_query,
        "disc_result_json": disc_result_json
    })
    try:
        context = dict(context, **{
            "group_filter": discs_group
        })
    except:
        pass
    return HttpResponse(template.render(context, request))