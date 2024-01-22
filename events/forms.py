from django import forms
from django.forms import ModelForm
from .models import Venue, Event, Star, Guest, Business, Booking, Wish

class GuestDetailForm(forms.ModelForm):
    BOOL_CHOICES = [(True, 'Yes'), (False, 'No')]
    is_business_guest = forms.BooleanField(
        widget=forms.RadioSelect(choices=BOOL_CHOICES),
        required=False
    )

    class Meta:
        model = Guest
        fields = ('first_name', 'last_name', 'email', 'phone')


class BusinessDetailForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name',)


class BookingDetailForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('room_type', 'date', 'number_of_nights')
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class ContactForm1(forms.Form):
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()

class ContactForm2(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

# Star
class StarForm(forms.ModelForm):
    class Meta:
        model = Star
        fields = ('first_name', 'last_name', 'email', 'phone')

# Admin SuperUser Event Form
class EventFormAdmin(ModelForm):
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


class EventForm(ModelForm):
    class Meta:
        model = Event
        # fields = "__all__"
        fields = ("name", "event_date", "venue", "description", "attendees")
        labels = {
            "name": "Venue",
            "event_date": "YYYY-MM-DD HH:MM:SS",
            "venue": "Venue",
            "description": "",
            "attendees": "Attendees",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Event Name"}),
            "event_date": forms.TextInput(attrs={"class": "form-control", "placeholder": "Event Date"}),
            "venue": forms.Select(attrs={"class": "form-select", "placeholder": "Venue"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
            "attendees": forms.SelectMultiple(attrs={"class": "form-control", "placeholder": "Attendees"}),
        }

# Create a venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        # fields = "__all__"
        fields = ("name", "address", "zip_code", "phone", "web", "email_address", "venue_image")
        labels = {
            "name": "Venue",
            "address": "",
            "zip_code": "",
            "phone": "",
            "web": "",
            "email_address": "",
            "venue_image": "",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Venue Name"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Venue Address"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Venue Zip Code"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Venue Phone Number"}),
            "web": forms.TextInput(attrs={"class": "form-control", "placeholder": "Venue Website URL"}),
            "email_address": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Venue Email Address"}),
        }

class WishForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your full name...'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your email...'}))
    phoneNumber = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your phone number...'}))

    class Meta:
        model = Wish
        fields = '__all__'