from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.user import User

class Visit:
    DB = 'exam_schema'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.tree_id = data['tree_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_visit(cls, data):
        query = "INSERT INTO visits (user_id, tree_id) VALUES (%(user_id)s, %(tree_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_visits_for_tree(cls, tree_id):
        query = "SELECT * FROM visits WHERE tree_id = %(tree_id)s;"
        data = {"tree_id": tree_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return [cls(result) for result in results]

    @classmethod
    def get_users_visits_to_tree(cls, tree_id):
        query = "SELECT users.* FROM users JOIN visits ON users.id = visits.user_id WHERE visits.tree_id = %(tree_id)s;"
        data = {"tree_id": tree_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return [User(result) for result in results]
    
    @classmethod
    def has_user_visited(cls, user_id, tree_id):
        query = "SELECT * FROM visits WHERE user_id = %(user_id)s AND tree_id = %(tree_id)s;"
        data = {'user_id': user_id, 'tree_id': tree_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return len(result) > 0
    
    @classmethod
    def remove_visit(cls, user_id, tree_id):
        query = "DELETE FROM visits WHERE user_id = %(user_id)s AND tree_id = %(tree_id)s;"
        data = {'user_id': user_id, 'tree_id': tree_id}
        connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_visit_count(cls, tree_id):
        query = "SELECT COUNT(*) AS count FROM visits WHERE tree_id = %(tree_id)s;"
        data = {'tree_id': tree_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result[0]['count'] if result else 0