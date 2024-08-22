from django import forms

from cdp_db_site_app.models import Group


# TODO: BUG: Attempting to edit a disc requires an image to be reuploaded
class DiscForm(forms.Form):
    title = forms.CharField(label="Title:", max_length=200)

    group = forms.ModelChoiceField(required=False, widget=forms.Select, queryset=Group.objects.all()
                                   , empty_label="No group", to_field_name="id")

    image = forms.ImageField(label="Image:", required=False)