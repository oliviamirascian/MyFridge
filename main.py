from google.appengine.api import urlfetch
import webapp2
import jinja2
import os
import json
from model import User
from webapp2_extras import sessions
from model import FoodFridge

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def getFoodID(response):
    if len(response) == 0:
        foodID = -1
        return foodID
    query = response[0]
    foodID = query["id"]
    return foodID

def getFoodInfo(response):
    name = response["name"]
    image = response["image"]

    # nutrition = foodBody.nutrition.nutrients.fetch()
    #
    # calories = {
    # 'title': nutrition[0].title,
    # 'amount': nutrition[0].amount,
    # 'unit': nutrition[0].unit,
    # 'percentOfDailyNeeds': nutrition[0].percentOfDailyNeeds
    # }
    #
    # saturatedFat = {
    # 'title': nutrition[2].title,
    # 'amount': nutrition[2].amount,
    # 'unit': nutrition[2].unit,
    # 'percentOfDailyNeeds': nutrition[2].percentOfDailyNeeds
    # }
    #
    # carbs = {
    # 'title': nutrition[3].title,
    # 'amount': nutrition[3].amount,
    # 'unit': nutrition[3].unit,
    # 'percentOfDailyNeeds': nutrition[3].percentOfDailyNeeds
    # }
    #
    # sugar = {
    # 'title': nutrition[4].title,
    # 'amount': nutrition[4].amount,
    # 'unit': nutrition[4].unit,
    # 'percentOfDailyNeeds': nutrition[4].percentOfDailyNeeds
    # }
    #
    # cholesterol = {
    # 'title': nutrition[5].title,
    # 'amount': nutrition[5].amount,
    # 'unit': nutrition[5].unit,
    # 'percentOfDailyNeeds': nutrition[5].percentOfDailyNeeds
    # }
    #
    # sodium = {
    # 'title': nutrition[6].title,
    # 'amount': nutrition[6].amount,
    # 'unit': nutrition[6].unit,
    # 'percentOfDailyNeeds': nutrition[6].percentOfDailyNeeds
    # }
    #
    # protein = {
    # 'title': nutrition[7].title,
    # 'amount': nutrition[7].amount,
    # 'unit': nutrition[7].unit,
    # 'percentOfDailyNeeds': nutrition[7].percentOfDailyNeeds
    # }
    #
    # fiber = {
    # 'title': nutrition[8].title,
    # 'amount': nutrition[8].amount,
    # 'unit': nutrition[8].unit,
    # 'percentOfDailyNeeds': nutrition[8].percentOfDailyNeeds
    # }

    foodInfo = [name,image]

    return foodInfo

class RecipeDisplayPage(webapp2.RequestHandler):
    def get(self):
        recipe_display_template = JINJA_ENVIRONMENT.get_template('templates/recipe_display.html')
        self.response.write(recipe_display_template.render())

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def isLoggedIn(self):
        if self.session.get('username') == "":
            return False
        return True

class MainPage(BaseHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())



        if self.isLoggedIn():
            self.redirect("/fridge")

    def post(self):
        fridge_template = JINJA_ENVIRONMENT.get_template('templates/fridge.html')
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')

        d = {
            'phrase': 'Incorrect password or username'
        }

        username = self.request.get('welcome_username')
        password = self.request.get('welcome_password')
        user_info = User.query().filter(username == User.username).fetch()

        if(len(user_info)>0):
            if password == user_info[0].password:
                self.redirect("/fridge")
                self.session['username'] = username
            else:
                self.response.write(welcome_template.render(d))

        else:
            self.response.write(welcome_template.render(d))


class CreateAccount(BaseHandler):
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

        user.put()

        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())




class FridgePage(BaseHandler):
    def get(self):
        fridge_template = JINJA_ENVIRONMENT.get_template('templates/fridge.html')
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        username = self.session.get('username')

        d = {
            'username': username
        }
        # checks if session username is  ""
        if self.isLoggedIn():
            self.response.write(fridge_template.render(d))
        else:
            self.response.write(welcome_template.render())
    def post(self):
        self.session['username'] = ""
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())

class FridgeFoodPage(BaseHanddler):
    def get(self):
        self.response.write(food)
    def post(self):
        body = json.loads(self.request.body)
        addFood = body['addFood']
        expirationDate = body['expirationDate']

        url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/autocomplete?query="+ addFood +"&number=1&metaInformation=true"

        response = urlfetch.fetch(url,
          headers={
            "X-Mashape-Key": "mJg6lyimB0mshXFRCjyqO6ZJ5mUup1xzQ4ijsnldTTcG83VyNc",
            "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
          }
        ).content
        json_response = json.loads(response)

        foodID = str(getFoodID(json_response))

        print foodID

        if foodID == "-1":
            return self.redirect("/notfound")
            return

        getFoodID(response)

        if foodID == -1:
            fridge_template = JINJA_ENVIRONMENT.get_template('templates/not_found.html')
            self.response.write(fridge_template.render())

        idUrl = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/"+ foodID +"/information?amount=1"

        response = urlfetch.fetch(idUrl,
          headers={
            "X-Mashape-Key": "mJg6lyimB0mshXFRCjyqO6ZJ5mUup1xzQ4ijsnldTTcG83VyNc",
            "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
          }
        ).content
        json_response = json.loads(response)

        name = getFoodInfo(json_response)[0]

        image = getFoodInfo(json_response)[1]

        food = FoodFridge(name=name,expirationDate=expirationDate,image=image)

        food.put()

        food_fridge = FoodFridge.query().fetch()

        fridge_variable_dict = {
        'food_name': name,
        'image': image,
        'expiration_date': expirationDate,
        'food_fridge': food_fridge
        }

        fridge_template = JINJA_ENVIRONMENT.get_template('templates/fridge.html')
        self.response.write(fridge_template.render())

class RemoveFridgePage(webapp2.RequestHandler):
    def get(self):
        remove_fridge_template = JINJA_ENVIRONMENT.get_template('templates/remove_fridge.html')
        self.response.write(remove_fridge_template.render())

    def post(self):
        removeFood = self.request.get("removeFood")
        del FoodFridge().removeFood

class NutriTrackerPage(BaseHandler):
    def get(self):
        nutriTracker_template = JINJA_ENVIRONMENT.get_template('templates/nutriTracker.html')
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        username = self.session['username']

        d = {
            'username': username
        }

        if self.isLoggedIn():
            self.response.write(nutriTracker_template.render(d))
            print self.session['username']
        else:
            self.response.write(welcome_template.render())
    def post(self):
        self.session['username'] = ""
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())

class RecipesPage(BaseHandler):
    def get(self):
        recipes_template = JINJA_ENVIRONMENT.get_template('templates/recipes.html')
        self.response.write(recipes_template.render())

    def post(self):
        search = self.request.get('search')

        url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?number=10&offset=0&query=" + search

        response = urlfetch.fetch(url,
  headers={
    "X-Mashape-Key": "mJg6lyimB0mshXFRCjyqO6ZJ5mUup1xzQ4ijsnldTTcG83VyNc",
    "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
  }
).content

        json_response = json.loads(response)

        results = json_response["results"][0]

        recipeID = results["id"]
        recipeTitle = results["title"]
        readyInMinutes = results["readyInMinutes"]
        servings = results["servings"]
        recipeImage = results["recipeImage"]

class NotFoundPage(webapp2.RequestHandler):
    def get(self):
        not_found_template = JINJA_ENVIRONMENT.get_template('templates/not_found.html')
        self.response.write(not_found_template.render())


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createAccount',CreateAccount),
    ('/fridge', FridgePage),
    ('/fridgefood', FridgeFoodPage),
    ('/removefridge', RemoveFridgePage),
    ('/nutritracker', NutriTrackerPage),
    ('/recipes', RecipesPage),
    ('/recipedisplay', RecipeDisplayPage),
    ('/notfound', NotFoundPage)
    ('/signIn', FridgePage)
], debug=True, config = config)
