from django import forms
from annoying.decorators import autostrip

@autostrip
class FbidForm(forms.Form):
    fbid = forms.IntegerField()
