from app import db, User, Recipe

# Create initial data
def create_initial_data():
    db.drop_all()
    db.create_all()
    
    user1 = User(name='John Doe', dietary_preferences='vegetarian')
    db.session.add(user1)
    
    recipe1 = Recipe(name='Pasta', ingredients='Pasta, Tomato Sauce, Cheese')
    recipe2 = Recipe(name='Salad', ingredients='Lettuce, Tomato, Cucumber, Olive Oil')
    
    db.session.add(recipe1)
    db.session.add(recipe2)
    
    db.session.commit()

if __name__ == '__main__':
    create_initial_data()
