from django.contrib import admin
from .models import Venue, MyClubUser, Event, Star, Business, Guest, Booking, Wish, Artist, Contact, Tour
from django.contrib.auth.models import Group

# admin.site.register(Venue)
admin.site.register(MyClubUser)
# Remove Groups
# admin.site.unregister(Group)
# admin.site.register(Event)
admin.site.register(Star)
admin.site.register(Business)
admin.site.register(Guest)
admin.site.register(Booking)
admin.site.register(Wish)
admin.site.register(Artist)
admin.site.register(Contact)
admin.site.register(Tour)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone")
    ordering = ("name",)
    search_fields = ("name", "address")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (("name", "venue"), "event_date", "description", "manager", "approved")
    list_display = ("name", "event_date", "venue")
    list_filter = ("event_date", "venue")
    ordering = ("-event_date",)