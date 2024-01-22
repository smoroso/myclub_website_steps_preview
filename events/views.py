from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue, Star, Booking, Business, Wish
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin, GuestDetailForm, BusinessDetailForm, BookingDetailForm, WishForm
from django.http import HttpResponse
import csv
from django.contrib import messages

# Import PDF Stuff
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import Pagination Stuff
from django.core.paginator import Paginator

# Formtools
from formtools.preview import FormPreview
from formtools.wizard.views import SessionWizardView
from django.forms.models import model_to_dict


class ContactWizard(SessionWizardView):
    # form_template = "events/add_star.html" # Not Working
    # preview_template = "events/add_star_preview.html" # Not Working
    # SessionWizardView.form_template = "events/add_star.html" # Not Working
    # SessionWizardView.preview_template = "events/add_star_preview.html" # Not Working
    # Note: Cannot combine stepped form and preview but maybe a last 'step' could be the preview
    template_name = "events/add_contact.html" # Works

    def done(self, form_list, form_dict, **kwargs):
        # 3 possibilities from tutorial (https://django-formtools.readthedocs.io/_/downloads/en/latest/pdf/)
        # 1- Do something and redirect
        # do_something_with_the_form_data(form_list)
        # return HttpResponseRedirect('/page-to-redirect-to-when-done/')

        # 2- Save form values
        # user = form_dict['user'].save()
        # credit_card = form_dict['credit_card'].save()

        # 3- Display a page with form values
        # return render(self.request, 'done.html', {
        #     'form_data': [form.cleaned_data for form in form_list],
        # })

        return redirect("list_stars")

def show_business_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('is_business_guest')

# Create your views here.
class BookingWizardView(SessionWizardView):
    form_list = [GuestDetailForm, BusinessDetailForm, BookingDetailForm]
    template_name = 'events/add_booking.html'
    condition_dict = {"1": show_business_form}

    # Used to set instance if we are updating
    def get_form_instance(self, step):
        if 'booking_id' in self.kwargs:
            booking_id = self.kwargs['booking_id']
            booking = Booking.objects.get(id=booking_id)
            if step == '0':
                return self.instance_dict.get(step, booking.guest)
            if step == '1':
                return  self.instance_dict.get(step, booking.guest.business)
            if step == '2':
                return  self.instance_dict.get(step, booking)

    # Used for adding some values to instantiate the form on top of default instance
    def get_form_initial(self, step):
        if 'booking_id' in self.kwargs:
            booking_id = self.kwargs['booking_id']
            booking = Booking.objects.get(id=booking_id)
            if step == '0':
                initial = self.initial_dict.get(step, {})
                initial.update({'is_business_guest': hasattr(booking.guest.business, 'name')}, **model_to_dict(booking.guest))
                return initial
        else:
            return self.initial_dict.get(step, {})

    def done(self, form_list, **kwargs):
        guest_form = form_list[0]
        guest = guest_form.save(commit=False)

        if guest_form.cleaned_data.get('is_business_guest'):
            business = form_list[1].save()
            guest.business = business
        else:
            if guest.business: # The guest changed it's mind and does not have a business
                guest.business = None

        guest.save()

        booking = form_list[-1].save(commit=False)
        booking.guest = guest
        booking.save()

        if 'booking_id' in self.kwargs:
            messages.success(self.request, ("Form submitted; Booking entry updated"))
        else:
            messages.success(self.request, ("Form submitted; Booking entry added"))
        return redirect("list_bookings")

# List Bookings
def list_bookings(request):
    booking_list = Booking.objects.all()

    # Set up pagination
    p = Paginator(Booking.objects.all(), 10)
    page = request.GET.get("page")
    bookings = p.get_page(page)
    nums = "a" * bookings.paginator.num_pages

    return render(request, "events/list_bookings.html", {
        "booking_list": booking_list,
        "bookings": bookings,
        "nums": nums,
    })


# Add Star
class StarFormPreview(FormPreview):
    form_template = "events/add_star.html"
    preview_template = "events/add_star_preview.html"

    def done(self, request, cleaned_data):
        Star.objects.create(**cleaned_data)
        messages.success(request, ("Form submitted; Star entry added"))
        return redirect("list_stars")

# List Stars
def list_stars(request):
    star_list = Star.objects.all()

    # Set up pagination
    p = Paginator(Star.objects.all(), 10)
    page = request.GET.get("page")
    stars = p.get_page(page)
    nums = "a" * stars.paginator.num_pages

    return render(request, "events/list_stars.html", {
        "star_list": star_list,
        "stars": stars,
        "nums": nums,
    })


def add_wish(request):
    form = WishForm()
    if request.method == 'POST':
        form = WishForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return redirect('preview_wish_postsave', pk=instance.id)
    context = {'form':form}
    return render(request, 'events/add_wish.html', context)

def preview_wish_postsave(request, pk):
    reg = Wish.objects.get(id=pk)
    prev = WishForm(instance=reg)
    if request.method == 'POST':
        form = WishForm(request.POST, instance=reg)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'reg':reg, 'prev':prev}
    return render(request, 'events/preview_wish_postsave.html', context)

# Show Event
def show_event(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, "events/show_event.html", {
        "event": event,
    })

# Show Events in a Venue
def venue_events(request, venue_id):
    # Grab the venue
    venue = Venue.objects.get(id=venue_id)
    # Grab the events from that venue
    events = venue.event_set.all()
    if events:
        return render(request, "events/venue_events.html", {
            "events": events,
        })
    else:
        messages.success(request, ("That venue has no events"))
        return redirect("admin_approval")


# Create Admin Event Approval Page
def admin_approval(request):
    # Get the venues
    venue_list = Venue.objects.all()
    # Get counts
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    event_list = Event.objects.all().order_by("-event_date")
    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist("boxes")
            # Uncheck all events (Hacky)
            event_list.update(approved=False)
            # Update the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request, ("Event List Approval has been updated"))
            return redirect("list-events")
        else:
            return render(request, "events/admin_approval.html", {
                "event_list": event_list,
                "event_count": event_count,
                "venue_count": venue_count,
                "user_count": user_count,
                "venue_list": venue_list,
            })
    else:
        messages.success(request, ("You aren't authorized to view this page"))
        return redirect("home")
    return render(request, "events/admin_approval.html", {})


# Create My Events Page
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees = me)
        return render(request, "events/my_events.html", {
            "events": events,
            "me": me,
        })
    else:
        messages.success(request, ("You aren't authorized to View this page"))
        return redirect("home")

# Generate a PDF File Venue List
def venue_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Designate the Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []
    # Loop
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")

    # Loop
    for line in lines:
        textob.textLine(line)
    
    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return something
    return FileResponse(buf, as_attachment=True, filename="venue.pdf")


# Generate CSV File Venue List
def venue_csv(request):
    response =  HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=venues.csv"

    # Create a csv writer
    writer = csv.writer(response)

    # Designate the Model
    venues = Venue.objects.all()

    # Add column headings to the csv file
    writer.writerow(["Venue name", "Address", "Zip Code", "Phone", "Web Address", "Email"])

    # Loop through and output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
    return response


# Generate Text File Venue List
def venue_text(request):
    response =  HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=venues.txt"
    # Designate the Model
    venues = Venue.objects.all()
    
    # Create blank list
    lines = []
    # Loop through and output
    for venue in venues:
        lines.append(f"{venue.name}-{venue.phone}\n")

    # Write to TextFie
    response.writelines(lines)
    return response

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect("list-venues")

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted!"))
        return redirect("list-events")
    else:
        messages.success(request, ("You aren't authorized to delete this event"))
        return redirect("list-events")

def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/add_event?submitted=True")
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user # logged in user
                event.save()
                return HttpResponseRedirect("/add_event?submitted=True")

    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if "submitted" in request.GET:
            submitted = True

    return render(request, "events/add_event.html", {
        "form": form,
        "submitted": submitted,
    })

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect("list-events")
    return render(request, "events/update_event.html", {
        "event": event,
        "form": form,
    })

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect("list-venues")
    return render(request, "events/update_venue.html", {
        "venue": venue,
        "form": form,
    })


def search_venues(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, "events/search_venues.html", {
            "searched": searched,
            "venues": venues,
        })
    else:
        return render(request, "events/search_venues.html", {})


def search_events(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        events = Event.objects.filter(description__contains=searched)
        return render(request, "events/search_events.html", {
            "searched": searched,
            "events": events,
        })
    else:
        return render(request, "events/search_events.html", {})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    venue = Venue.objects.get(id=venue_id)
    # Grab the events from that venue
    events = venue.event_set.all()
    return render(request, "events/show_venue.html", {
        "venue": venue,
        "venue_owner": venue_owner,
        "events": events,
    })


def list_venues(request):
    # venue_list = Venue.objects.all().order_by("?") # could be database intensive
    venue_list = Venue.objects.all()

    # Set up pagination
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get("page")
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages

    return render(request, "events/venue.html", {
        "venue_list": venue_list,
        "venues": venues,
        "nums": nums,
    })

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            venue = form.save(commit=False)
            venue.owner = request.user.id # logged in user
            venue.save()
            return HttpResponseRedirect("/add_venue?submitted=True")
    else:
        form = VenueForm
        if "submitted" in request.GET:
            submitted = True

    return render(request, "events/add_venue.html", {
        "form": form,
        "submitted": submitted,
    })


def all_events(request):
    event_list = Event.objects.all().order_by("-event_date", "-name", "venue")
    return render(request, "events/event_list.html", {
        "event_list": event_list,
    })


def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    month = month.capitalize()
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # Create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # Get current year
    now = datetime.now()
    current_year = now.year

    # Query the Events Model for Dates
    event_list = Event.objects.filter(
        event_date__year = year,
        event_date__month = month_number,
    )

    # Get current time
    time = now.strftime("%I:%M:%S %p")

    return render(request, "events/home.html", {
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
        "event_list": event_list,
    })