from django import forms



class announces(forms.Form):
    textarea = forms.CharField(label='Textarea',max_length=300)
    material = forms.URLField(label='Material',max_length=100)



    