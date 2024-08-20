"""
URL configuration for cdp_db_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.template.defaulttags import url
from django.urls import path
from django.views.static import serve

from cdp_db_site import settings
from cdp_db_site_app import views

urlpatterns = [
    path("discs/<int:position>", views.api.list_specific_disc, name="List specific disc"),
    path("discs/all", views.api.list_all_discs, name="List all discs"),
    path("groups/all", views.api.list_all_groups, name="List all groups"),
    path("discs/ingroup/<int:group>", views.api.list_discs_in_specific_group, name="List discs in a specific group"),
    path("groups/new", views.api.create_group, name="Create a new group"),
    path("groups/edit/<int:group>", views.api.edit_group, name="Edit a specific group"),
    path("groups/remove/<int:group>", views.api.remove_group, name="Delete a specific group"),
    path("discs/edit/<int:position>", views.api.json_add_edit_disc, name="Add or edit a disc via JSON"),
    path("discs/remove/<int:position>", views.api.remove_disc, name="Remove a disc"),
    path("control/<int:position>", views.api.send_control_command, name="Send a control command to the CDP"),

    path("", views.pages.index, name="Homepage"),
    path("<int:position>", views.pages.index, name="Homepage, but scrolled to a position"),

    path("edit/<int:position>", views.pages.edit, name="Edit page for a specific disc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)