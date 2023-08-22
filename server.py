from flask_app import app
from flask_app.controllers import trees, users, visits

if __name__ == "__main__":
    app.run(debug=True)

