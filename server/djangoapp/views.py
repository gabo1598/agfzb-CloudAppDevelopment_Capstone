from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,get_list_or_404, render, redirect
from .models import CarModel, CarMake, DealerReview
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    
# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context={}
    if request.method == "GET":
        st = ""
        url = "https://223ee29a.us-south.apigw.appdomain.cloud/captson/dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url,st)
        context['dealerships'] = dealerships
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context['dealer_names'] = dealer_names
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)
        #return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context={}
    if request.method == "GET":
        url = "https://223ee29a.us-south.apigw.appdomain.cloud/captson/reviews"
        
        reviews = get_dealer_reviews_from_cf(url,dealer_id)
        context['reviews'] = reviews
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)
        #return HttpResponse(reviews)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    print(f"dealer_id en view{dealer_id}")
    context = {}
    if request.method == "GET":
        url = "https://223ee29a.us-south.apigw.appdomain.cloud/captson/dealerships"
        dealerships = get_dealers_from_cf(url,"")
        for dealer in dealerships:
            if dealer.id == dealer_id:
                dealership = dealer
        car = get_list_or_404(CarModel, Dealer_id=dealer_id)
        context["dealer_id"] = dealer_id
        context["cars"] = car
        context["dealership"] = dealership
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        url = "https://223ee29a.us-south.apigw.appdomain.cloud/captson/reviews"
        params={}
        if request.POST["purchase"] == "1":
            params["name"] = f"{request.user.first_name} {request.user.last_name}"
            params["dealership"] = dealer_id
            params["review"] = request.POST["review"]
            params["purchase"] = True
            params["purchase_date"] = request.POST["purchase_date"]
            car = request.POST["car"].split("-")
            params["car_make"] = car[1]
            params["car_model"] = car[0]
            params["car_year"] = car[2]
        else:
            params["name"] = f"{request.user.first_name} {request.user.last_name}"
            params["dealership"] = dealer_id
            params["review"] = request.POST["review"]
            params["purchase"] = False
        review = {"review":params}
        print(request.POST["purchase"])
        response = post_request(url,review,dealer_id=dealer_id)
        if response:
            print(response)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)