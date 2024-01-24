from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Star(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=12)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Artist(models.Model):
    first_name = models.CharField('First Name', max_length=120)
    last_name = models.CharField('Last Name', max_length=120)

    def __str__(self):
        return self.first_name

class Contact(models.Model):
    subject = models.CharField('Subject', max_length=120)
    message = models.TextField('Message')

    def __str__(self):
        return self.subject

class Tour(models.Model):
    name = models.CharField('Tour summary', max_length=120)
    description = models.TextField('Description', max_length=120, null=True)
    departure_date = models.DateTimeField('Departure Date', default=date.today())
    arrival_date = models.DateTimeField('Arrival Date', default=date.today())
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=True, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Contact Phone', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Adress', blank=True)
    owner = models.IntegerField("Venue Owner", blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete = models.CASCADE)
    # venue = models.CharField(max_length=120)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)
    approved = models.BooleanField("Approved", default=False)

    def __str__(self):
        return self.name

    @property
    def Days_till(self):
        today = date.today()
        days_till = self.event_date.date() - today
        days_till_stripped = str(days_till).split(",", 1)[0]
        return days_till_stripped
    
    @property
    def Is_Past(self):
        today = date.today()
        if self.event_date.date() < today:
            thing = "Past"
        else:
            thing = "Future"
        return thing


# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Guest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Booking(models.Model):
    class RoomTypes(models.TextChoices):
        SINGLE = "Single"
        DOUBLE = "Double"
        FAMILY = "Family"

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
    room_type = models.CharField(max_length=10, choices=RoomTypes.choices)
    date = models.DateField()
    number_of_nights = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.guest.full_name}: {self.number_of_nights} nights in {self.room_type} room"

class Wish(models.Model):
    regChoice = (
        ('Self', 'Self'),
        ('Group', 'Group'),
        ('Corporate', 'Corporate'),
        ('Others', 'Others'),
    )
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254,null=True)
    phoneNumber =  models.CharField(max_length=15,null=True)
    idCard = models.ImageField(null=True)
    regType = models.CharField(max_length=25, choices=regChoice,null=True)
    ticketNo = models.IntegerField(default=1)

    def __str__(self):
        return self.name