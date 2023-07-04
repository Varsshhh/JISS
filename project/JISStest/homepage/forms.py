from .models import user_details
from django import forms

class get_user(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = user_details
        fields = ['username','password']
