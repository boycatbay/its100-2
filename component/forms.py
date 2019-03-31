from django import forms


class announces(forms.Form):
    textarea = forms.CharField(label='textarea',max_length=300)
    material = forms.CharField(label='material',max_length=100)
