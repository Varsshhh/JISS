from django.contrib.auth.models import User
from django import forms
from .models import identity,keyword

class resolved_case_details(forms.ModelForm):

    class Meta:
        model = identity
        fields=[
            'cin'
            ]
        
class resolved_case_details_keyword(forms.ModelForm):

    class Meta:
        model = keyword
        fields=[
            'keyword'
            ]