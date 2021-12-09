import requests
import json
from .models import CarDealer,DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests

def post_request(url,json_payload,**kwargs):
    print(json_payload)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url,json=json_payload,params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")
    

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url,st, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,st=st)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"],state=dealer_doc["state"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url,dealership, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,dealership=dealership)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["reviews"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            # Create a CarDealer object with values in `doc` object
            if review_doc["purchase"]:
                review_obj = DealerReview(id=review_doc["id"], dealership=review_doc["dealership"],
                name=review_doc["name"],purchase=review_doc["purchase"], review=review_doc["review"],
                purchase_date=review_doc["purchase_date"],car_make=review_doc["car_make"],
                car_model=review_doc["car_model"], car_year=review_doc["car_year"],
                sentiment="placeholder")
            else:
                review_obj = DealerReview(id=review_doc["id"], dealership=review_doc["dealership"],
                name=review_doc["name"],purchase=review_doc["purchase"], review=review_doc["review"],
                purchase_date="NULL",car_make="NULL", car_model="NULL", car_year="NULL",
                sentiment="placeholder")
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
  url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2c9067dd-ba8f-4519-915e-dda091771fc6"
  apikey = "zGXIJ39HpSzOQxJZhOmnqC1nnUUiXo33smsmX4WeytOU"
  
  authenticator = IAMAuthenticator(f'{apikey}')
  natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01', authenticator=authenticator)

  natural_language_understanding.set_service_url(f'{url}')
  try:
    response = natural_language_understanding.analyze(text=text,
      features=Features(sentiment=SentimentOptions())).get_result()
    respuesta1 = response["sentiment"]
    respuesta2 = respuesta1["document"]
    return(respuesta2["label"])
  except:
      return("neutral")