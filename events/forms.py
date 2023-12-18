from django import forms
from django.forms import ModelForm
from .models import Venue, Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        # fields = "__all__"
        fields = ("name", "event_date", "venue", "manager", "description", "attendees")
        labels = {
            "name": "Venue",
            "event_date": "YYYY-MM-DD HH:MM:SS",
            "venue": "Venue",
            "manager": "Manager",
            "description": "",
            "attendees": "Attendees",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Event Name"}),
            "event_date": forms.TextInput(attrs={"class": "form-control", "placeholder": "Event Date"}),
            "venue": forms.Select(attrs={"class": "form-select", "placeholder": "Venue"}),
            "manager": forms.Select(attrs={"class": "form-select", "placeholder": "Manager"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
            "attendees": forms.SelectMultiple(attrs={"class": "form-control", "placeholder": "Attendees"}),
        }

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