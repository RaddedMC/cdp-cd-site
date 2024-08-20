from django import forms

from cdp_db_site_app.models import Group


class DiscForm (forms.Form):
    title = forms.CharField(label="Title:", max_length=200)

    choices = *((group.pk, group.title) for group in Group.objects.all()), ("null", "No group")
    group = forms.ChoiceField(choices=choices)

    image = forms.ImageField(label="Image:")
