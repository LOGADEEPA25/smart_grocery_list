from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    dietary_preferences = db.Column(db.String(200))

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ingredients = db.Column(db.String(500))

class GroceryList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.Column(db.String(500))

db.create_all()

# RESTful API Resources
class RecipeResource(Resource):
    def get(self):
        recipes = Recipe.query.all()
        return jsonify([{'id': recipe.id, 'name': recipe.name, 'ingredients': recipe.ingredients} for recipe in recipes])

class GroceryListResource(Resource):
    def get(self, user_id):
        grocery_list = GroceryList.query.filter_by(user_id=user_id).first()
        if grocery_list:
            return jsonify({'items': grocery_list.items})
        return jsonify({'message': 'Grocery list not found'})

    def post(self, user_id):
        data = request.get_json()
        items = data.get('items')
        grocery_list = GroceryList(user_id=user_id, items=items)
        db.session.add(grocery_list)
        db.session.commit()
        return jsonify({'message': 'Grocery list created'})

api.add_resource(RecipeResource, '/recipes')
api.add_resource(GroceryListResource, '/grocerylist/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
