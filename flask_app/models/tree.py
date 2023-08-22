from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask_app.models.user import User
from flask import flash

class Tree:
    DB = 'exam_schema'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.date_planted = data['date_planted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.visits = None
        #self.comments=None
#Create
    @classmethod
    def create_tree(cls, data):
        query = """
                    INSERT INTO trees (user_id, species, location, reason, date_planted) 
                    VALUES ( %(user_id)s,  %(species)s, %(location)s, %(reason)s, %(date_planted)s);
        
        """
        # data is a dictionary that will be passed into the save method from server.py
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_tree(data):
        is_valid = True  # We assume this is true
        
        if len(data['species']) < 5:
            flash("Species is required.")
            is_valid = False
        if len(data['location']) < 2:
            flash("Location is required.")
            is_valid = False
        if len(data['reason']) < 50:
            flash("A reason for planting must be 50 characters. Put some thought into it!")
            is_valid = False
        if not data['date_planted']:
            flash("Date planted is required.")
            is_valid = False

        
        return is_valid
# #READ
#             #This is not a normal one to many route this will select all and is good for posting to a wall.
    @classmethod
    def get_all_trees_with_creator(cls):
            # Get all tweets, and their one associated User that created it
            query = "SELECT * FROM trees JOIN users ON trees.user_id = users.id;"
            results = connectToMySQL(cls.DB).query_db(query)
            all_trees = []
            for row in results:
                # Create a Tweet class instance from the information from each db row
                one_tree = cls(row)
                # Prepare to make a User class instance, looking at the class in models/user.py
                one_trees_author_info = {
                    # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                    "id": row['users.id'], 
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at']
                }
                # Create the User class instance that's in the user.py model file
                author = User(one_trees_author_info)
                # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
                one_tree.creator = author
                # Append the Tweet containing the associated User to your list of tweets
                all_trees.append(one_tree)
            return all_trees
    @classmethod
    def get_tree_by_id_with_creator(cls, tree_id):
        query = """
            SELECT * FROM trees 
            JOIN users ON trees.user_id = users.id 
            WHERE trees.id = %(tree_id)s;
        """
        data = {"tree_id": tree_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        if result:
            tree_data = result[0]
            creator_data = {
                "id": tree_data['users.id'],
                "first_name": tree_data['first_name'],
                "last_name": tree_data['last_name'],
                "email": tree_data['email'],
                "password": tree_data['password'],
                "created_at": tree_data['created_at'],
                "updated_at": tree_data['updated_at']
            }
            creator = User(creator_data)
            
            tree = cls(tree_data)  # Create a tree instance
            tree.creator = creator  # Associate the creator User instance with the tree
            return tree
        else:
            return None
    @classmethod
    def get_trees_by_user_id(cls, user_id):
        query = """
            SELECT * FROM trees
            WHERE user_id = %(user_id)s;
        """
        data = {"user_id": user_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        trees = []
        for tree_data in result:
            tree = cls(tree_data)
            trees.append(tree)
        
        return trees

#update
    @classmethod
    def edit_tree(cls, data):
        query = """
            UPDATE trees
            SET 
                species = %(species)s,
                location = %(location)s,
                reason = %(reason)s,
                date_planted = %(date_planted)s
            WHERE id = %(id)s;
        """
        
        return connectToMySQL(cls.DB).query_db(query, data)
#delete
    @classmethod
    def delete_tree(cls, tree_id):
        query = "DELETE FROM trees WHERE id = %(tree_id)s;"
        data = {"tree_id": tree_id}
        return connectToMySQL(cls.DB).query_db(query, data)

