from django import forms

from cdp_db_site_app.models import Group


# TODO: BUG: Attempting to edit a disc requires an image to be reuploaded
class DiscForm(forms.Form):
    title = forms.CharField(label="Title:", max_length=200)

    choices = ("null", "No group"), *((group.pk, group.title) for group in Group.objects.all())
    group = forms.ChoiceField(choices=choices)

    image = forms.ImageField(label="Image:", required=False)