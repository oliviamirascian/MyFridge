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
        username = self.session.get('username')
        time.sleep(.250)
        if self.isLoggedIn():
            user = User.query().filter(username == User.username).fetch()[0]
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
        print(response)
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




            # food_fridge = FoodFridge.query().fetch()
            #
            # fridge_variable_dict = {
            # 'food_name': name,
            # 'image': image,
            # 'expiration_date': expirationDate,
            # 'food_fridge': food_fridge,
            # }
            #
            # fridge_template = JINJA_ENVIRONMENT.get_template('templates/fridge.html')
            # self.response.write(fridge_template.render(fridge_variable_dict))
            self.redirect("/fridge")

class RemoveFridgePage(BaseHandler):
    def get(self):
        remove_fridge_template = JINJA_ENVIRONMENT.get_template('templates/remove_fridge.html')
        self.response.write(remove_fridge_template.render())


    def post(self):
        removeFood = self.request.get("removeFood")
        del FoodFridge().removeFood

# class NutriTrackerPage(BaseHandler):
#     def get(self):
#         nutriTracker_template = JINJA_ENVIRONMENT.get_template('templates/nutriTracker.html')
#         welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
#         username = self.session.get('username')
#
#         d = {
#             'username': username
#         }
#
#         if self.isLoggedIn():
#             self.response.write(nutriTracker_template.render(d))
#             print self.session.get('username')
#         else:
#             self.response.write(welcome_template.render())
#     def post(self):
#         self.session['username'] = ""
#         welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
#         self.response.write(welcome_template.render())



class RecipesPage(BaseHandler):
    def get(self):
        recipes_template = JINJA_ENVIRONMENT.get_template('templates/recipes.html')
        username = self.session.get('username')
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
                    "X-Mashape-Key": "1JtCtxBW9UmshioZoOu5KHTJq7nop19lNHVjsnzbMCzcmil9Hb",
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
                print(result.content)
                food_images = list(map(lambda x: (x["title"],x["image"]), json.loads(result.content)))#makes it an array of image urls
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
        recipe = Recipe(name = name,
                        picture = picture)
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

        keys = user.recipes
        recipe_models_list = []
        recipes_name = []
        for i in keys:
            model = i.get()
            if model:
                if model.name not in recipes_name:
                    recipe_models_list.append(model)
                    recipes_name.append(model.name)

        d = {'all_recipe_models' : recipe_models_list}
        self.response.write(recipes_template.render(d))

RECIPE_API_URL_TEMPLATE = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients=false&limitLicense=false&number=5&ranking=1&ingredients={}"

# class RecipesDisplay(BaseHandler):
#     def get(self):
#         recipes_template = JINJA_ENVIRONMENT.get_template('templates/recipes.html')
#         username = self.session.get('username')
#         if self.isLoggedIn():
#             user = User.query().filter(username == User.username).fetch()[0]
#             keys = user.recipes
#             recipe_models_list = []
#             recipes_name = []
#             for i in keys:
#                 model = i.get()
#                 if model:
#                     if model.name not in recipes_name:
#                         recipes_name.append(model.name)
#                         recipe_models_list.append(model)
#
#             d = {'all_recipe_models' : recipe_models_list,
#                 'username': username
#             }
#
#             food_keys = user.fridge_foods
#             food_names_list = []
#             for i in food_keys:
#                 model = i.get()
#                 food_names_list.append(model.name)
#             ingredients = ""
#             for i in food_names_list:
#                 ingredients = ingredients + i + " "
#             # ingredients = self.request.get('food')
#             if "," not in ingredients:
#                 url = RECIPE_API_URL_TEMPLATE.format(ingredients.replace(' ', '%2C'))
#             else:
#                 url = RECIPE_API_URL_TEMPLATE.format(ingredients.replace(',', '%2C').replace(' ', ''))
#             result = urlfetch.fetch(
#                 url=url,
#                 headers={
#                     "X-Mashape-Key": "1JtCtxBW9UmshioZoOu5KHTJq7nop19lNHVjsnzbMCzcmil9Hb",
#                     "Accept": "application/json"
#                 },
#                 validate_certificate=True,#makes website more secuire
#                 method=urlfetch.GET,#get request
#                 deadline=30# gives it at most 30 seconds until it errors
#             )
#
#             # [ { recipe info 1 }, {recipe info 2},...]
#             # the map operates on each element individually
#             # x is first { recipe info 1 }, turning it into [img name], then x is { recipe info 2},...
#             # so then becomes [ [img name 1], [img name 2] ]
#
#             # 200 means it's good
#             if result.status_code == 200:
#                 print(result.content)
#                 food_images = list(map(lambda x: (x["title"],x["image"]), json.loads(result.content)))#makes it an array of image urls
#                 self.response.write(recipes_template.render(food_images=food_images,**d))
#                 # do stuff you want
#             else:
#                 self.response.write("oops an api call error occured")
#                 # handle the error
#         else:
#             self.redirect('/')
#     def post(self):
#         pass

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
            if model.name != recipe:
                print model.name
                print recipe
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
                    for i in recipe_models_list:
                        recipes_name.append(i.name)
                    if model.name not in recipes_name:
                        recipe_models_list.append(model)

            d = {'all_recipe_models' : recipe_models_list,
                'username': username
            }
            self.response.write(recipes_template.render(d))
        else:
            self.redirect("/")





        # sandy.key.delete()




class RecipeInstrucionsPage(BaseHandler):
    def get(self):
        recipeInstructions_template = JINJA_ENVIRONMENT.get_template('templates/recipe_display.html')
        self.response.write(recipeInstructions_template.render())
        recipe = self.request.get('recipeName')



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
    ('/removefridge', RemoveFridgePage),
    # ('/nutritracker', NutriTrackerPage),
    ('/recipes', RecipesPage),
    # ('/recipesdisplay', RecipesDisplay),
    ('/notfound', NotFoundPage),
    ('/signIn', FridgePage),
    ('/recipeInstructions',RecipeInstrucionsPage),
    ('/removeRecipe', RemoveRecipe)
], debug=True, config = config)
