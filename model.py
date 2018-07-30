from google.appengine.ext import ndb

class Food(ndb.Model):
    name = ""
    date_entered = time.time()

    
