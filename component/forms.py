from django import forms
from .classroomAccessAPI import getcousreList
from django.db import models
class announces(forms.Form):
    textarea = forms.CharField(label='Textarea',max_length=300)
    material = forms.URLField(label='Material',max_length=100)

class courseSelect(models.Model):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(courseSelect, self).__init__(*args, **kwargs)
        cousrelist = getcousreList(request)
        choie = ()
        for cous in cousrelist:
            choie +=((cous['name'],cous['id']),)
        couserSel =  models.CharField(max_length=len(choie)+1,choices=choie, default=choie[0][1])
        