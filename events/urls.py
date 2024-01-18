from django.urls import path
from . import views
from .forms import StarForm, ContactForm1, ContactForm2
from .views import ContactWizard

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:year>/<str:month>/", views.home, name="home"),
    path("events", views.all_events, name="list-events"),
    path("add_venue", views.add_venue, name="add-venue"),
    path("list_venues", views.list_venues, name="list-venues"),
    path("show_venue/<venue_id>", views.show_venue, name="show-venue"),
    path("search_venues", views.search_venues, name="search-venues"),
    path("update_venue/<venue_id>", views.update_venue, name="update-venue"),
    path("update_event/<event_id>", views.update_event, name="update-event"),
    path("add_event", views.add_event, name="add-event"),
    path("delete_event/<event_id>", views.delete_event, name="delete-event"),
    path("delete_venue/<venue_id>", views.delete_venue, name="delete-venue"),
    path("venue_text", views.venue_text, name="venue-text"),
    path("venue_csv", views.venue_csv, name="venue-csv"),
    path("venue_pdf", views.venue_pdf, name="venue-pdf"),
    path("my_events", views.my_events, name="my_events"),
    path("search_events", views.search_events, name="search_events"),
    path("admin_approval", views.admin_approval, name="admin_approval"),
    path("venue_events/<venue_id>", views.venue_events, name="venue-events"),
    path("show_event/<event_id>", views.show_event, name="show-event"),
    path("add_star", views.StarFormPreview(StarForm), name="add_star"),
    path("list_stars", views.list_stars, name="list_stars"),
    path('add_contact/', ContactWizard.as_view([ContactForm1, ContactForm2]), name="add_contact"),
    path('add_booking/', views.BookingWizardView.as_view(), name="add_booking"),
    path("list_bookings", views.list_bookings, name="list_bookings"),
]
