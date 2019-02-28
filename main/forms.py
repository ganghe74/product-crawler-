from django import forms
from .models import Subscriber
from datetime import datetime
class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('expiry_date', 'email', 'min_price', 'max_price')
        widgets = {
            'expiry_date': forms.DateInput(attrs={'readonly': True, 'value': '3000-01-01'})
        }