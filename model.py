from google.appengine.ext import ndb
from datetime import time

class FoodFridge(ndb.Model):
    name = ndb.StringProperty(required=True)
    #format of expiration dates: "YYYY-MM-DD" ex. "2017-06-01"
    expirationDate = ndb.StringProperty(required=True)
    image = ""

    # calories = ""
    # saturatedFat = ""
    # carbs = ""
    # sugar = ""
    # cholesterol = ""
    # sodium = ""
    # protein = ""
    # fiber = ""

    def __init__(self, name, expirationDate, image):
        self.name = name
        self.expirationDate = expirationDate
        self.image = image
        # self.calories = calories
        # self.saturatedFat = saturatedFat
        # self.carbs = carbs
        # self.sugar = sugar
        # self.cholesterol = cholesterol
        # self.sodium = sodium
        # self.protein = protein
        # self.fiber = fiber

class User(ndb.Model):
    first_name = ndb.StringProperty(required = True)
    last_name = ndb.StringProperty(required = True)
    username = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
