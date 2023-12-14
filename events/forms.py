from django import forms
from django.forms import ModelForm
from .models import Venue


# Create a venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        # fields = "__all__"
        fields = ("name", "address", "zip_code", "phone", "web", "email_address")
        labels = {
            "name": "Venue",
            "address": "",
            "zip_code": "",
            "phone": "",
            "web": "",
            "email_address": "",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Venue Name"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Venue Address"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Venue Zip Code"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Venue Phone Number"}),
            "web": forms.TextInput(attrs={"class": "form-control", "placeholder": "Venue Website URL"}),
            "email_address": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Venue Email Address"}),
        }