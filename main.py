from google.appengine.api import urlfetch
import webapp2
import jinja2
import os
from model import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

<<<<<<< HEAD
# def foodInDB(response):
#     foodQuery = response.query()
#
#     foodBody = foodQuery.root.body.fetch()
#
#     if foodBody[0] == "":
#         window.alert("That food is not in our database. Check for spelling errors.")
#     else:


=======
>>>>>>> working sign in
class MainPage(webapp2.RequestHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())

    def post(self):
        print("I'M IN POST!")
        self.redirect("/fridge")
        fridge_template = JINJA_ENVIRONMENT.get_template('templates/fridge.html')
        username = self.request.get('welcome_username')
        password = self.request.get('welcome_password')
        user_info = User.query().filter(username == User.username).fetch()
        if (username == user_info[0].username) and (password == user_info[0].password):
            self.response.write(fridge_template.render())
            self.redirect("/fridge")




class CreateAccount(webapp2.RequestHandler):
    def get(self):
        createAccount_template = JINJA_ENVIRONMENT.get_template('templates/createAccount.html')
        self.response.write(createAccount_template.render())

    def post(self):
        first_name = self.request.get('FirstName')
        last_name = self.request.get('LastName')
        username = self.request.get('Username')
        password = self.request.get('Password')

        user = User(first_name = first_name,
                    last_name = last_name,
                    username = username,
                    password = password)
        print ("Something")
        user.put()





class FridgePage(webapp2.RequestHandler):
    def get(self):
        fridge_template = JINJA_ENVIRONMENT.get_template('templates/fridge.html')
        self.response.write(fridge_template.render())

class NutriTrackerPage(webapp2.RequestHandler):
    def get(self):
        nutriTracker_template = JINJA_ENVIRONMENT.get_template('templates/nutriTracker.html')
        self.response.write(nutriTracker_template.render())

class RecipesPage(webapp2.RequestHandler):
    def get(self):
        recipes_template = JINJA_ENVIRONMENT.get_template('templates/recipes.html')
        self.response.write(recipes_template.render())

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createAccount',CreateAccount),
    ('/fridge', FridgePage),
    ('/nutritracker', NutriTrackerPage),
    ('/recipes', RecipesPage)
], debug=True)
