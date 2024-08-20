import colorfield.fields
from django import forms

from cdp_db_site_app.models import Group

class GroupForm(forms.Form):
    title = forms.CharField(label="Title:", max_length=200)
    color = forms.CharField(label="Color:", max_length=7)