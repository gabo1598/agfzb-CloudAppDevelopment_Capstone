from django.db import models
from django.utils.timezone import now

# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=200, default="add name here")
    description = models.CharField(max_length=200, default="add description here")
    def __str__ (self):
        return 'name: ' + self.name + ' \nDescription: ' + self.description


class CarModel(models.Model):
    maker = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="add name here")
    Dealer_id = models.IntegerField(default=0)
    class Type_of_car(models.TextChoices):
       SEDAN = 'sd' , 'Sedan'
       SUV = 'sv' , 'SUV'
       WAGON = 'wg' , 'Wagon'
       PICKUP = 'pt' , 'Pickup Truck'
       MINIVAN = 'mv' , 'Minivan'
       CONVERTIBLE = 'cv' , 'Convertible'
       HATCHBACK = 'hb' , 'Hatchback'
       COUPE = 'cp' , 'Coupe'
       SPORTS = 'sc' , 'Sports Car'
    
    carType =  models.CharField(max_length=2, choices = Type_of_car.choices, default=Type_of_car.SEDAN)
    year = models.DateField(null=True, default = now)
    def __str__ (self):
        return f"Manufacturer: {self.maker}\nName: {self.name}\nDealer: {self.Dealer_id}\nType: {self.carType}\nYear: {self.year}" 

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, state,address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.state = state
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self,id,name,dealership,review,purchase,purchase_date,car_make,car_model,car_year,sentiment):
        self.id = id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
    def __str__(self):
        return "name: " + self.name + "\nreview: " + self.review


# <HINT> Create a plain Python class `DealerReview` to hold review data
