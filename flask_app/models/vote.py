from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.user import User

class Vote:
    DB = 'exam_schema'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.pie_id = data['pie_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_vote(cls, data):
        query = "INSERT INTO votes (user_id, pie_id) VALUES (%(user_id)s, %(pie_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_votes_for_pie(cls, pie_id):
        query = "SELECT * FROM votes WHERE pie_id = %(pie_id)s;"
        data = {"pie_id": pie_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return [cls(result) for result in results]

    # @classmethod
    # def get_users_votes_to_pie(cls, pie_id):
    #     query = "SELECT users.* FROM users JOIN votes ON users.id = votes.user_id WHERE votes.pie_id = %(pie_id)s;"
    #     data = {"pie_id": pie_id}
    #     results = connectToMySQL(cls.DB).query_db(query, data)
    #     return [User(result) for result in results]
    
    @classmethod
    def get_users_votes_to_pie(cls, pie_id, user_id):
        query = """
            SELECT * FROM votes
            WHERE pie_id = %(pie_id)s AND user_id = %(user_id)s;
        """
        data = {
            "pie_id": pie_id,
            "user_id": user_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        
        votes = []
        for row in results:
            votes.append(cls(row))
        
        return votes

    @classmethod
    def has_user_voted(cls, user_id, pie_id):
        query = "SELECT * FROM votes WHERE user_id = %(user_id)s AND pie_id = %(pie_id)s;"
        data = {'user_id': user_id, 'pie_id': pie_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return len(result) > 0
    
    @classmethod
    def remove_vote(cls, user_id, pie_id):
        query = "DELETE FROM votes WHERE user_id = %(user_id)s AND pie_id = %(pie_id)s;"
        data = {'user_id': user_id, 'pie_id': pie_id}
        connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_vote_count(cls, pie_id):
        query = "SELECT COUNT(*) AS count FROM votes WHERE pie_id = %(pie_id)s;"
        data = {'pie_id': pie_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result[0]['count'] if result else 0