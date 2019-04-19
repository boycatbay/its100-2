from django import forms



class announces(forms.Form):
    textarea = forms.CharField(label='Textarea',max_length=300)
    material = forms.CharField(label='Material',max_length=100)

class uploads(forms.Form):
    title = forms.CharField(label='Assignment Title',max_length=100)
    description = forms.CharField(label='Assignment Description',max_length=300)
    scores = forms.IntegerField(label='Maximum Scores')
    material = forms.CharField(label='Materials',max_length=300)
 



    