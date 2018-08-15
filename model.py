from google.appengine.ext import ndb
from datetime import time

class FoodFridge(ndb.Model):
    name = ndb.StringProperty(required=True)
    #format of expiration dates: "YYYY-MM-DD" ex. "2017-06-01"
    expirationDate = ndb.StringProperty(required=True)
    image = ndb.StringProperty(required=True)

class Recipe(ndb.Model):
    name = ndb.StringProperty(required = True)
    picture = ndb.StringProperty(required = True)
    id = ndb.StringProperty(required = True)

class User(ndb.Model):
    first_name = ndb.StringProperty(required = True)
    last_name = ndb.StringProperty(required = True)
    username = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
    fridge_foods = ndb.KeyProperty(FoodFridge, repeated = True)
    recipes = ndb.KeyProperty(Recipe, repeated = True)
