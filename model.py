from google.appengine.ext import ndb
from datetime import time

class FoodFridge(ndb.Model):
    name = ndb.StringProperty(required=True)
    #format of expiration dates: "YYYY-MM-DD" ex. "2017-06-01"
    expirationDate = ndb.StringProperty(required=True)
    image = ""

    calories = ""
    fat = ""
    saturatedFat = ""
    carbs = ""
    sugar = ""
    cholesterol = ""
    sodium = ""
    protein = ""
    fiber = ""
    iron = ""
    calcium = ""

    # vitaminC = ""
    # vitaminK = ""
    # vitaminB6 = ""
    # vitaminB2 = ""
    # vitaminE = ""
    # vitaminB1 = ""
    # vitaminA = ""
    # vitaminB5 = ""

    def __init__(self, calories, fat, saturatedFat, carbs, sugar, cholesterol, sodium, protein, fiber, potassium, iron, calcium):
        self.calories = calories
        self.fat = fat
        self.saturatedFat = saturatedFat
        self.carbs = carbs
        self.sugar = sugar
        self.cholesterol = cholesterol
        self.sodium = sodium
        self.protein = protein
        self.fiber = fiber
        self.potassium = potassium
        self.iron = iron
        self.calcium = calcium

class User(ndb.Model):
    first_name = ndb.StringProperty(required = True)
    last_name = ndb.StringProperty(required = True)
    username = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
