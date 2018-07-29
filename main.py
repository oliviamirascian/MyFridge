import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

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
    ('/', FridgePage),
    ('/nutritracker', NutriTrackerPage),
    ('/recipes', RecipesPage)
], debug=True)
