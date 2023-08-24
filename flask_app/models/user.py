# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from email_validator import validate_email, EmailNotValidError
from flask import flash, session
class User:
    DB = 'exam_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.pies = []
        # self.comments=[]
        self.votes = []

    # Now we use class methods to query our database
#Create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

#get user by id
    @classmethod
    def get_one(cls, id):
        query = """
        SELECT * from users
        WHERE id = %(id)s
        """
        return connectToMySQL(cls.DB).query_db(query, {"id": id})
    #get all users for the friends add

    @classmethod
    def get_all_users(cls):
        logged_in_user_id = session['user_id']
        query = "SELECT * FROM users WHERE id != %s;"
        users_except_logged_in = connectToMySQL(cls.DB).query_db(query, (logged_in_user_id,))

        # make sure to call the connectToMySQL function with the schema you are targeting.
        
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in users_except_logged_in:
            users.append(cls(user))
        return users
    
    

#         # Static methods don't have self or cls passed into the parameters.
#     # We do need to take in a parameter to represent our burger
    @staticmethod
    def validate_user(user):
        is_valid = True  # We assume this is true

        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False

        # Email validation using email_validator library
        try:
            validate_email(user['email'])
        except EmailNotValidError:
            flash("Please enter a valid email address.")
            is_valid = False
        existing_user = User.get_by_email({"email": user['email']})
        if existing_user:
            flash("A user with this email already exists.")
            is_valid = False
        # Password validation: Check for at least one capital, one number, one special character
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        elif not any(char.isupper() for char in user['password']):
            flash("Password must contain at least one uppercase letter.")
            is_valid = False
        elif not any(char.isdigit() for char in user['password']):
            flash("Password must contain at least one digit.")
            is_valid = False
        elif not any(char in "!@#$%^&*()_-+=<>?/[]}{|/\~" for char in user['password']):
            flash("Password must contain at least one special character.")
            is_valid = False
        elif user['password'] != user['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False

        return is_valid


    @classmethod
    def get_votes_by_user(cls, id):
        query = """
            SELECT vote.id AS vote_id, vote.first_name, vote.last_name
            FROM users
            LEFT JOIN votes ON users.id = votes.user_id
            LEFT JOIN users vote ON votes.vote_id = vote.id
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, {'id': id})

        votes = []
        for row in results:
            vote_id = row['vote_id']
            vote_first_name = row['first_name']
            vote_last_name = row['last_name']

            vote_info = {
                "id": vote_id,
                "first_name": vote_first_name,
                "last_name": vote_last_name
            }
            vote = User(vote_info)
            votes.append(vote)

        if not votes:  # Check if the list is empty
            return None

        return votes

    @classmethod
    def get_votes_by_pie(cls, id):
        query = """
            SELECT vote.first_name
            FROM users
            LEFT JOIN votes ON users.id = votes.user_id
            LEFT JOIN users vote ON votes.vote_id = vote.id
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, {'id': id})

        votes = []
        for row in results:
            vote_user_name = row['first_name']
            votes.append(vote_user_name)

        return votes