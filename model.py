from google.appengine.ext import ndb

class FoodFridge(ndb.Model):
    name = ndb.StringProperty(required=True)
    #format of expiration dates: "YYYY-MM-DD" ex. "2017-06-01"
    expirationDate = ndb.StringProperty(required=True)
