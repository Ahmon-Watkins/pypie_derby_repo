from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask_app.models.user import User
from flask import flash

class Pie:
    DB = 'exam_schema'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.votes = None
        #self.comments=None
#Create
    @classmethod
    def create_pie(cls, data):
        query = """
                    INSERT INTO pies (user_id, name, filling, crust) 
                    VALUES ( %(user_id)s,  %(name)s, %(filling)s, %(crust)s);
        
        """
        # data is a dictionary that will be passed into the save method from server.py
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_pie(data):
        is_valid = True  # We assume this is true
        
        if len(data['name']) < 3:
            flash("Name is required.")
            is_valid = False
        if len(data['filling']) < 3:
            flash("Filling is required.")
            is_valid = False
        if len(data['crust']) < 3:
            flash("A crust is required")
            is_valid = False

        return is_valid
# #READ
#             #This is not a normal one to many route this will select all and is good for posting to a wall.
    @classmethod
    def get_all_pies_with_creator(cls):
            # Get all tweets, and their one associated User that created it
            query = "SELECT * FROM pies JOIN users ON pies.user_id = users.id;"
            results = connectToMySQL(cls.DB).query_db(query)
            all_pies = []
            for row in results:
                # Create a Tweet class instance from the information from each db row
                one_pie = cls(row)
                # Prepare to make a User class instance, looking at the class in models/user.py
                one_pies_author_info = {
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
                author = User(one_pies_author_info)
                # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
                one_pie.creator = author
                # Append the Tweet containing the associated User to your list of tweets
                all_pies.append(one_pie)
            return all_pies
    @classmethod
    def get_pie_by_id_with_creator(cls, pie_id):
        query = """
            SELECT * FROM pies 
            JOIN users ON pies.user_id = users.id 
            WHERE pies.id = %(pie_id)s;
        """
        data = {"pie_id": pie_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        if result:
            pie_data = result[0]
            creator_data = {
                "id": pie_data['users.id'],
                "first_name": pie_data['first_name'],
                "last_name": pie_data['last_name'],
                "email": pie_data['email'],
                "password": pie_data['password'],
                "created_at": pie_data['created_at'],
                "updated_at": pie_data['updated_at']
            }
            creator = User(creator_data)
            
            pie = cls(pie_data)  # Create a pie instance
            pie.creator = creator  # Associate the creator User instance with the pie
            return pie
        else:
            return None
    @classmethod
    def get_pies_by_user_id(cls, user_id):
        query = """
            SELECT * FROM pies
            WHERE user_id = %(user_id)s;
        """
        data = {"user_id": user_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        pies = []
        for pie_data in result:
            pie = cls(pie_data)
            pies.append(pie)
        
        return pies

#update
    @classmethod
    def edit_pie(cls, data):
        query = """
            UPDATE pies
            SET 
                name = %(name)s,
                filling = %(filling)s,
                crust = %(crust)s
            WHERE id = %(id)s;
        """
        
        return connectToMySQL(cls.DB).query_db(query, data)
#delete
    @classmethod
    def delete_pie(cls, pie_id):
        query = "DELETE FROM pies WHERE id = %(pie_id)s;"
        data = {"pie_id": pie_id}
        return connectToMySQL(cls.DB).query_db(query, data)

