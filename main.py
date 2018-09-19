from google.appengine.api import urlfetch
import webapp2
import jinja2
import os
import json
import time
from webapp2_extras import sessions
from model import FoodFridge,Recipe,User

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

    foodInfo = [name,image]

    return foodInfo



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
        if self.session.get('username') == "" or self.session.get('username') is None:
            return False
        return True

class MainPage(BaseHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')



        if self.isLoggedIn():
            self.redirect("/aboutus")
        else:
            self.response.write(welcome_template.render())

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

class AboutUs(BaseHandler):
    def get(self):
        AboutUs_template = JINJA_ENVIRONMENT.get_template('templates/AboutUs.html')
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')


        username = self.session.get('username')

        d = {
            'username':username
        }
        if self.isLoggedIn():
            self.response.write(AboutUs_template.render(d))
        else:

            self.redirect("/")

    def post(self):
        pass


class CreateAccount(BaseHandler):
    def get(self):
        createAccount_template = JINJA_ENVIRONMENT.get_template('templates/createAccount.html')
        self.response.write(createAccount_template.render())

    def post(self):
        createAccount_template = JINJA_ENVIRONMENT.get_template('templates/createAccount.html')
        first_name = self.request.get('FirstName')
        last_name = self.request.get('LastName')
        username = self.request.get('Username')
        password = self.request.get('Password')

        d = {
            'exists': 'The username already exists.'
        }
        if len(User.query().filter(username == User.username).fetch()) == 0:
            user = User(first_name = first_name,
                        last_name = last_name,
                        username = username,
                        password = password)
            user.put()
            self.redirect('/')
        else:
            self.response.write(createAccount_template.render(d))

class FridgePage(BaseHandler):
    def get(self):
        fridge_template = JINJA_ENVIRONMENT.get_template('templates/fridge.html')
        username = self.session.get('username')
        time.sleep(.250)
        if self.isLoggedIn():
            user = User.query().filter(username == User.username).fetch()[0]
            keys = user.fridge_foods

            food_fridge = []
            for i in keys:
                model = i.get()
                if model:
                    food_fridge.append(model)


            d = {
                'username': username,
                'food_fridge': food_fridge
            }
            # checks if session username is  ""

            self.response.write(fridge_template.render(d))
        else:
            self.redirect("/")
    def post(self):
        self.session['username'] = ""
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())

class FridgeFoodPage(BaseHandler):
    def post(self):
        addFood = self.request.get('addFood')
        expirationDate = self.request.get('expirationDate')

        if expirationDate == "":
            expirationDate = " "

        if " " in addFood:
            urlFood = addFood.replace(" ", "-")
        else:
            urlFood = addFood

        url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/autocomplete?query="+ urlFood +"&number=1&metaInformation=true"

        response = urlfetch.fetch(url,
          headers={
            "X-Mashape-Key": "mJg6lyimB0mshXFRCjyqO6ZJ5mUup1xzQ4ijsnldTTcG83VyNc",
            "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
          }
        ).content
        json_response = json.loads(response)

        foodID = str(getFoodID(json_response))
        if foodID == "-1":
            fridge_template = JINJA_ENVIRONMENT.get_template('templates/not_found.html')
            self.response.write(fridge_template.render())
        else:

            idUrl = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/"+ foodID +"/information?amount=1"

            response = urlfetch.fetch(idUrl,
              headers={
                "X-Mashape-Key": "mJg6lyimB0mshXFRCjyqO6ZJ5mUup1xzQ4ijsnldTTcG83VyNc",
                "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
              }
            ).content
            json_response = json.loads(response)

            name = getFoodInfo(json_response)[0]

            image = "https://spoonacular.com/cdn/ingredients_100x100/" + getFoodInfo(json_response)[1]

            food = FoodFridge(name=name,expirationDate=expirationDate,image=image)



            #just key
            food_key = food.put()
            #whole recipe model
            #finds user
            username = self.session.get('username')
            user = User.query().filter(username == User.username).fetch()[0]

            #store in database
            user.fridge_foods.append(food_key)
            user.put()

            self.redirect("/fridge")

class RemoveFridgePage(BaseHandler):
    def post(self):
        fridge_template = JINJA_ENVIRONMENT.get_template('templates/fridge.html')
        expirationDate = self.request.get('expirationDate')
        food = self.request.get('foodName')
        username = self.session.get('username')
        user = User.query().filter(username == User.username).fetch()[0]
        food_keys = user.fridge_foods
        for i in food_keys:
            model = i.get()
            if model:
                if (model.name == food) and (model.expirationDate == expirationDate):
                    food_keys.remove(i)
                    break


        user.fridge_foods = food_keys
        user.put()
        # self.response.write(fridge_template.render())

        #parting thing

        time.sleep(.250)
        keys = user.fridge_foods
        # user = User.query().filter(username == User.username).fetch()[0]
        # keys = user.recipes
        # recipe_models_list = []
        # recipes_name = []
        # for i in keys:
        #     model = i.get()
        #     if model:
        #         for i in recipe_models_list:
        #             recipes_name.append(i.name)
        #         if model.name not in recipes_name:
        #             recipe_models_list.append(model)

        food_fridge = []
        for i in keys:
            model = i.get()
            if model:
                food_fridge.append(model)
        d = {
            'username': username,
            'food_fridge': food_fridge
        }
        # checks if session username is  ""
        self.response.write(fridge_template.render(d))

RECIPE_API_URL_TEMPLATE = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients=false&limitLicense=false&number=5&ranking=1&ingredients={}"
class RecipesPage(BaseHandler):
    def get(self):
        recipes_template = JINJA_ENVIRONMENT.get_template('templates/recipes.html')
        username = self.session.get('username')
        time.sleep(.250)
        if self.isLoggedIn():
            user = User.query().filter(username == User.username).fetch()[0]
            keys = user.recipes
            recipe_models_list = []
            recipes_name = []
            for i in keys:
                model = i.get()
                if model:
                    if model.name not in recipes_name:
                        recipes_name.append(model.name)
                        recipe_models_list.append(model)

            d = {'all_recipe_models' : recipe_models_list,
                'username': username
            }

            food_keys = user.fridge_foods
            food_names_list = []
            for i in food_keys:
                    model = i.get()
                    if model:
                        food_names_list.append(model.name)
            ingredients = ""
            for i in food_names_list:
                ingredients = ingredients + i + " "
            # ingredients = self.request.get('food')
            if "," not in ingredients:
                url = RECIPE_API_URL_TEMPLATE.format(ingredients.replace(' ', '%2C'))
            else:
                url = RECIPE_API_URL_TEMPLATE.format(ingredients.replace(',', '%2C').replace(' ', ''))
            result = urlfetch.fetch(
                url=url,
                headers={
                    # "X-Mashape-Key": "1JtCtxBW9UmshioZoOu5KHTJq7nop19lNHVjsnzbMCzcmil9Hb",
                    # "Accept": "application/json"
                    "X-Mashape-Key": "mJg6lyimB0mshXFRCjyqO6ZJ5mUup1xzQ4ijsnldTTcG83VyNc",
                    "Accept": "application/json"
                },
                validate_certificate=True,#makes website more secuire
                method=urlfetch.GET,#get request
                deadline=30# gives it at most 30 seconds until it errors
            )

            # [ { recipe info 1 }, {recipe info 2},...]
            # the map operates on each element individually
            # x is first { recipe info 1 }, turning it into [img name], then x is { recipe info 2},...
            # so then becomes [ [img name 1], [img name 2] ]

            # 200 means it's good
            if result.status_code == 200:
                food_images = list(map(lambda x: (x["title"],x["image"],x["id"]), json.loads(result.content)))#makes it an array of image urls
                self.response.write(recipes_template.render(food_images=food_images,**d))
                # do stuff you want
            else:
                self.response.write("oops an api call error occured")
                # handle the error
        else:
            self.redirect('/')
    def post(self):
        recipes_template = JINJA_ENVIRONMENT.get_template('templates/recipes.html')
        name = self.request.get('recipe_name')
        picture = self.request.get('recipe_picture')
        id = self.request.get('recipeID')
        recipe = Recipe(name = name,
                        picture = picture,
                        id = id)
        #just key
        recipe_key = recipe.put()
        #whole recipe model
        recipe_model = recipe_key.get()
        #finds user
        username = self.session.get('username')
        user = User.query().filter(username == User.username).fetch()[0]

        #store in database
        user.recipes.append(recipe_key)
        user.put()

        self.redirect("/recipes?")

class RemoveRecipe(BaseHandler):
    def post(self):
        recipes_template = JINJA_ENVIRONMENT.get_template('templates/recipes.html')
        recipe = self.request.get('recipe')
        username = self.session.get('username')
        user = User.query().filter(username == User.username).fetch()[0]
        recipe_keys = user.recipes
        new_recipe_keys = []
        for i in recipe_keys:
            model = i.get()
            if model:
                if model.name != recipe:
                    new_recipe_keys.append(i)

        user.recipes = new_recipe_keys
        user.put()

        if self.isLoggedIn():
            keys = user.recipes
            recipe_models_list = []
            recipes_name = []
            for i in keys:
                model = i.get()
                if model:
                    if model.name not in recipes_name:
                        recipes_name.append(model.name)
                        recipe_models_list.append(model)

            d = {'all_recipe_models' : recipe_models_list,
                'username': username
            }

            food_keys = user.fridge_foods
            food_names_list = []
            for i in food_keys:
                    model = i.get()
                    if model:
                        food_names_list.append(model.name)
            ingredients = ""
            for i in food_names_list:
                ingredients = ingredients + i + " "
            # ingredients = self.request.get('food')
            if "," not in ingredients:
                url = RECIPE_API_URL_TEMPLATE.format(ingredients.replace(' ', '%2C'))
            else:
                url = RECIPE_API_URL_TEMPLATE.format(ingredients.replace(',', '%2C').replace(' ', ''))
            result = urlfetch.fetch(
                url=url,
                headers={
                    "X-Mashape-Key": "mJg6lyimB0mshXFRCjyqO6ZJ5mUup1xzQ4ijsnldTTcG83VyNc",
                    "Accept": "application/json"
                },
                validate_certificate=True,#makes website more secuire
                method=urlfetch.GET,#get request
                deadline=30# gives it at most 30 seconds until it errors
            )

            # [ { recipe info 1 }, {recipe info 2},...]
            # the map operates on each element individually
            # x is first { recipe info 1 }, turning it into [img name], then x is { recipe info 2},...
            # so then becomes [ [img name 1], [img name 2] ]

            # 200 means it's good
            if result.status_code == 200:
                food_images = list(map(lambda x: (x["title"],x["image"], x["id"]), json.loads(result.content)))#makes it an array of image urls
                self.response.write(recipes_template.render(food_images=food_images,**d))
                # do stuff you want
            else:
                self.response.write("oops an api call error occured")
                # handle the error
        else:
            self.redirect('/')

recipe_instructions_url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/analyzedInstructions?stepBreakdown=true"
recipe_ingredients_url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information?includeNutrition=false"
class PossibleRecipes(BaseHandler):
    def get(self):
        recipeID = self.request.get('recipe_id')
        url = recipe_instructions_url.format(recipeID)
        url1 = recipe_ingredients_url.format(recipeID)
        result = urlfetch.fetch(
            url = url,
            headers={
                "X-Mashape-Key": "mJg6lyimB0mshXFRCjyqO6ZJ5mUup1xzQ4ijsnldTTcG83VyNc",
                "Accept": "application/json"
              },
          validate_certificate = True,
          method = urlfetch.GET,
          deadline = 30
        )

        result1 = urlfetch.fetch(
            url = url1,
            headers={
                "X-Mashape-Key": "mJg6lyimB0mshXFRCjyqO6ZJ5mUup1xzQ4ijsnldTTcG83VyNc",
                "Accept": "application/json"
            },
            validate_certificate = True,
            method = urlfetch.GET,
            deadline = 30
        )

        if (result.status_code == 200) and len(json.loads(result.content)) > 0:
            #ingredients
            json_response1 = json.loads(result1.content)
            ingredients = json_response1["extendedIngredients"]
            self.response.write("<br><br> <a href = \"/recipes\">Back to Recipes Page </a> <br><br>")
            self.response.write("Ingredients:" + "<br><br>")
            for ingredient in ingredients:
                self.response.write(ingredient["name"] + " ")
                self.response.write(str(ingredient["amount"]) + " ")
                self.response.write(ingredient["unit"])
                self.response.write("<br>")
            #recipeInstructions
            self.response.write("<br>")
            json_response = json.loads(result.content)[0]
            steps = json_response["steps"]
            self.response.write("<br> Recipe Instructions: <br> <br>")
            counter = 1
            for i in steps:
                self.response.write("Step:" + str(counter))
                counter+=1
                self.response.write("<br>")
                self.response.write(i["step"])
                self.response.write("<br>")
        else:
            self.response.write("sorry, recipe does not exist <br>")
            self.response.write("<a href = \"/recipes\">Back to Recipes Page </a")

search_recipe_url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?instructionsRequired=true&number=5&offset=0&query={}"
class RecipesSearch(BaseHandler):
    def get(self):
        recipe_search_template = JINJA_ENVIRONMENT.get_template('templates/recipe_search.html')
        recipe = self.request.get('the_recipe')
        recipe = recipe.replace(' ', '+')
        url = search_recipe_url.format(recipe)
        result = urlfetch.fetch(
            url = url,
            headers = {
                "X-Mashape-Key": "mJg6lyimB0mshXFRCjyqO6ZJ5mUup1xzQ4ijsnldTTcG83VyNc",
                "Accept": "application/json"
            },
            validate_certificate = True,
            method = urlfetch.GET,
            deadline = 30
        )
        self.response.write("<br><br> <a href = \"/recipes\">Back to Recipes Page </a>")
        if result.status_code == 200:
            recipe_information = list(map(lambda x: (x["title"],x["readyInMinutes"],x["id"],x["image"]), json.loads(result.content)["results"]))
            self.response.write(recipe_search_template.render(recipe_information = recipe_information))
        else:
            self.response.write("sorry, recipe does not exist")
            self.response.write("<a href = \"/recipes\">Back to Recipes Page </a")


class NotFoundPage(BaseHandler):
    def get(self):
        not_found_template = JINJA_ENVIRONMENT.get_template('templates/not_found.html')
        self.response.write(not_found_template.render())


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/aboutus', AboutUs),
    ('/createAccount',CreateAccount),
    ('/fridge', FridgePage),
    ('/fridgefood', FridgeFoodPage),
    ('/removeFood', RemoveFridgePage),
    # ('/nutritracker', NutriTrackerPage),
    ('/recipes', RecipesPage),
    # ('/recipesdisplay', RecipesDisplay),
    ('/notfound', NotFoundPage),
    ('/signIn', FridgePage),
    ('/recipeInstructions',PossibleRecipes),
    ('/removeRecipe', RemoveRecipe),
    ('/getRecipe', RecipesSearch)
], debug=True, config = config)
